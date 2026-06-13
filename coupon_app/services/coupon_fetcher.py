import logging
import os
import re
import ssl
import urllib.request
from datetime import datetime

import certifi
import feedparser

logger = logging.getLogger(__name__)

CATEGORY_KEYWORDS = [
    ("Food", ["food", "pizza", "restaurant", "grocery", "dining", "eat", "burger", "coffee"]),
    ("Hair & Beauty", ["hair", "beauty", "salon", "spa", "cosmetic", "makeup"]),
    ("Fashion", ["shoe", "clothes", "fashion", "dress", "apparel", "wear", "jeans"]),
    ("Electronics", ["laptop", "phone", "electronic", "tech", "computer", "gadget", "tablet"]),
    ("Travel", ["travel", "flight", "hotel", "car rental", "airfare", "vacation", "cruise"]),
    ("Pets", ["pet", "dog", "cat"]),
    ("Health", ["health", "vitamin", "gym", "fitness", "pharmacy", "wellness"]),
]
DEFAULT_CATEGORY = "Shopping"

# Word-boundary matching - plain substring checks misfire on short keywords
# like "cat"/"pet" matching inside unrelated words (e.g. "dealcatcher.com",
# which appears in every DealCatcher feed entry's image URL).
_CATEGORY_PATTERNS = [
    (category, re.compile("|".join(r"\b" + re.escape(keyword) + r"\b" for keyword in keywords), re.IGNORECASE))
    for category, keywords in CATEGORY_KEYWORDS
]

# Only the "code"/"promo code" keyword is case-insensitive - the captured
# code itself must be upper-case/digits, otherwise e.g. "code that" matches
# the lowercase word "that" as a bogus code under IGNORECASE.
CODE_PATTERN = re.compile(r"(?i:code|promo code|coupon code)[:\s]+([A-Z0-9]{4,15})\b")

# feedparser uses urllib under the hood, which on some Python installs (notably
# python.org builds on macOS) has no CA bundle wired up and fails every HTTPS
# fetch with a certificate-verify error. Pin it to certifi's bundle explicitly
# so feeds aren't silently treated as "blocked or unavailable".
_HTTPS_HANDLER = urllib.request.HTTPSHandler(context=ssl.create_default_context(cafile=certifi.where()))

# Some feeds (notably Reddit) return 429 for the default Python user-agent.
_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}


def categorize(*texts):
    combined = " ".join(t for t in texts if t)
    for category, pattern in _CATEGORY_PATTERNS:
        if pattern.search(combined):
            return category
    return DEFAULT_CATEGORY


def _parse_published(entry):
    """Convert feedparser's UTC time.struct_time into a naive UTC datetime."""
    parsed_time = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed_time:
        return None
    return datetime(*parsed_time[:6])


class Provider:
    name = "base"

    def fetch(self):
        raise NotImplementedError


class MockProvider(Provider):
    """Always-available sample data so the pipeline works with zero API keys configured."""

    name = "mock"

    SAMPLE = [
        {"store": "Mock Outlet", "title": "20% off your first order", "code": "MOCK20", "discount": "20%", "url": "https://example.com/mock-outlet"},
        {"store": "Demo Grocers", "title": "$10 off $50 grocery order", "code": "DEMO10", "discount": "$10", "url": "https://example.com/demo-grocers"},
        {"store": "Sample Travel Co", "title": "Save $75 on flight bookings", "code": "FLY75DEMO", "discount": "$75", "url": "https://example.com/sample-travel"},
    ]

    def fetch(self):
        return [{**item, "source": self.name} for item in self.SAMPLE]


class RSSFeedProvider(Provider):
    """Parses free deal RSS feeds with feedparser.

    Many deal sites block scrapers (Cloudflare etc.), drop their feed URLs, or
    have DNS/availability issues, so a feed returning nothing is logged as a
    warning and skipped rather than treated as a hard failure.
    """

    name = "rss"

    DEFAULT_FEEDS = [
        "https://slickdeals.net/newsearch.php?mode=frontpage&frontpage=1&rss=1",
        "https://slickdeals.net/newsearch.php?mode=popdeals&rss=1",
        "https://www.reddit.com/r/deals/.rss",
        "https://www.reddit.com/r/coupons/.rss",
        "https://www.reddit.com/r/frugal/.rss",
        "https://hip2save.com/feed/",
        "https://www.passionatepennypincher.com/feed/",
        "https://www.dealcatcher.com/rss",
    ]

    ENTRIES_PER_FEED = 50

    def __init__(self, feed_urls=None):
        if feed_urls is not None:
            self.feed_urls = feed_urls
        else:
            env_feeds = os.environ.get("RSS_FEED_URLS")
            self.feed_urls = [u.strip() for u in env_feeds.split(",") if u.strip()] if env_feeds else self.DEFAULT_FEEDS

    def fetch(self):
        results = []
        for url in self.feed_urls:
            try:
                parsed = feedparser.parse(url, handlers=[_HTTPS_HANDLER], request_headers=_REQUEST_HEADERS)
            except Exception:
                logger.exception("Failed to fetch RSS feed %s", url)
                continue

            if not parsed.entries:
                logger.warning("RSS feed returned no entries (blocked or unavailable): %s", url)
                continue

            for entry in parsed.entries[: self.ENTRIES_PER_FEED]:
                title = getattr(entry, "title", "").strip()
                if not title:
                    continue
                description = getattr(entry, "summary", "")

                code_match = CODE_PATTERN.search(f"{title} {description}")
                store = (title.split(":")[0].split(" - ")[0]).strip()[:120] or "Unknown Store"

                results.append({
                    "store": store,
                    "title": title,
                    "code": code_match.group(1).upper() if code_match else "SEEONSITE",
                    "discount": "",
                    "url": getattr(entry, "link", ""),
                    "description": description,
                    "published_at": _parse_published(entry),
                    "source": self.name,
                })

            logger.info("RSS feed %s returned %d entries", url, len(parsed.entries))
        return results


def get_providers():
    return [MockProvider(), RSSFeedProvider()]


def fetch_coupons(providers=None):
    providers = get_providers() if providers is None else providers

    raw = []
    for provider in providers:
        try:
            items = provider.fetch()
        except Exception:
            logger.exception("Provider %s failed", provider.name)
            continue
        logger.info("Provider %s returned %d coupon(s)", provider.name, len(items))
        raw.extend(items)

    for item in raw:
        item.setdefault("category", categorize(item.get("title", ""), item.get("store", ""), item.get("description", "")))
        item.setdefault("states", ["All"])
        item.setdefault("cities", ["All"])
        item.setdefault("expires_at", None)
        item.setdefault("discount", "")
        item.setdefault("url", "")

    return raw
