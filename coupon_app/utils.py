from datetime import datetime, timezone


def utcnow():
    """Naive UTC datetime - matches what SQLite stores, so comparisons stay simple."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def parse_expiry(value):
    """Parse 'Jul 31, 2025' / 'YYYY-MM-DD' / ISO strings into a naive UTC datetime, or None."""
    if not value:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    for fmt in ("%b %d, %Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def format_expiry(value):
    """Format a datetime back into the 'Jul 31, 2025' style the templates expect."""
    if not value:
        return "No expiry"
    return value.strftime("%b %d, %Y")
