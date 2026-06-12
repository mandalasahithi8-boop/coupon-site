import logging
from datetime import timedelta

from coupon_app.data import SEED_COUPONS
from coupon_app.extensions import db
from coupon_app.models import Category, Coupon, Store
from coupon_app.utils import parse_expiry, utcnow

logger = logging.getLogger(__name__)


def _future_expiry(expires_str):
    """Seed data has fixed date strings from when this catalog was written.

    Shift any that have since fallen into the past forward by whole years so a
    fresh deploy doesn't start with every seed coupon already expired and hidden.
    """
    expires_at = parse_expiry(expires_str)
    if expires_at is None:
        return None
    now = utcnow()
    while expires_at < now:
        expires_at += timedelta(days=365)
    return expires_at


def seed_database():
    """Load the original 44 curated coupons into Store/Category/Coupon tables."""
    added = 0
    for item in SEED_COUPONS:
        store = Store.query.filter_by(name=item["store"]).first()
        if not store:
            store = Store(name=item["store"], logo=item["logo"], url=item["url"])
            db.session.add(store)
            db.session.flush()

        category = Category.query.filter_by(name=item["category"]).first()
        if not category:
            category = Category(name=item["category"])
            db.session.add(category)
            db.session.flush()

        if Coupon.query.filter_by(store_id=store.id, code=item["code"]).first():
            continue

        db.session.add(Coupon(
            store=store,
            category=category,
            title=item["title"],
            code=item["code"],
            discount=item["discount"],
            url=item["url"],
            states=item["states"],
            cities=item["cities"],
            expires_at=_future_expiry(item["expires"]),
            source="seed",
            is_active=True,
            verified=True,
        ))
        added += 1

    db.session.commit()
    logger.info("Seeded %d coupons (%d already present)", added, len(SEED_COUPONS) - added)
    return added


def seed_if_empty():
    if Coupon.query.first() is None:
        seed_database()
