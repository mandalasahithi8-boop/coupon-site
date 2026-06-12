import logging

from coupon_app.extensions import db
from coupon_app.models import Category, Coupon, RefreshLog, Store
from coupon_app.services.coupon_fetcher import fetch_coupons
from coupon_app.utils import utcnow

logger = logging.getLogger(__name__)


def _get_or_create_store(name, logo=None, url=None):
    store = Store.query.filter_by(name=name).first()
    if not store:
        store = Store(name=name, logo=logo or "🏷️", url=url or "")
        db.session.add(store)
        db.session.flush()
    return store


def _get_or_create_category(name):
    category = Category.query.filter_by(name=name).first()
    if not category:
        category = Category(name=name)
        db.session.add(category)
        db.session.flush()
    return category


def save_coupons(raw_coupons):
    """Upsert fetched coupons, deduplicated by (store, code). Returns (created, updated)."""
    created = 0
    updated = 0

    for item in raw_coupons:
        store = _get_or_create_store(item["store"], item.get("logo"), item.get("url"))
        category = _get_or_create_category(item["category"])

        existing = Coupon.query.filter_by(store_id=store.id, code=item["code"]).first()
        if existing:
            existing.title = item["title"]
            existing.discount = item.get("discount", existing.discount)
            existing.url = item.get("url") or existing.url
            existing.category = category
            existing.expires_at = item.get("expires_at") or existing.expires_at
            existing.is_active = True
            updated += 1
        else:
            db.session.add(Coupon(
                store=store,
                category=category,
                title=item["title"],
                code=item["code"],
                discount=item.get("discount", ""),
                url=item.get("url", ""),
                states=item.get("states", ["All"]),
                cities=item.get("cities", ["All"]),
                expires_at=item.get("expires_at"),
                source=item.get("source", "unknown"),
                is_active=True,
                verified=item.get("source") == "seed",
                # Falls back to the column default (utcnow) when the source has no date.
                created_at=item.get("published_at"),
            ))
            created += 1

    db.session.commit()
    return created, updated


def deactivate_expired():
    """Mark coupons whose expires_at is in the past as inactive. Returns count deactivated."""
    now = utcnow()
    expired = Coupon.query.filter(
        Coupon.expires_at.isnot(None),
        Coupon.expires_at < now,
        Coupon.is_active.is_(True),
    ).all()
    for coupon in expired:
        coupon.is_active = False
    db.session.commit()
    return len(expired)


def cleanup_duplicates():
    """Remove duplicate (store_id, code) rows, keeping the most recently created. Returns count removed."""
    seen = set()
    removed = 0
    for coupon in Coupon.query.order_by(Coupon.created_at.desc()).all():
        key = (coupon.store_id, coupon.code)
        if key in seen:
            db.session.delete(coupon)
            removed += 1
        else:
            seen.add(key)
    db.session.commit()
    return removed


def run_full_refresh(source="manual"):
    """Fetch from all providers, save, deactivate expired, dedupe, and log the run."""
    raw = fetch_coupons()
    created, updated = save_coupons(raw)
    deactivated = deactivate_expired()
    duplicates = cleanup_duplicates()

    log = RefreshLog(
        source=source,
        fetched=len(raw),
        created=created,
        updated=updated,
        deactivated=deactivated,
        duplicates_removed=duplicates,
    )
    db.session.add(log)
    db.session.commit()

    result = {
        "fetched": len(raw),
        "created": created,
        "updated": updated,
        "deactivated": deactivated,
        "duplicates_removed": duplicates,
        "ran_at": log.ran_at.isoformat() + "Z",
    }
    logger.info("Coupon refresh (%s): %s", source, result)
    return result
