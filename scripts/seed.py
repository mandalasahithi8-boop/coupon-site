"""Run with: python3 -m scripts.seed
Loads the original 44 coupons into the database (skips any already present)."""

from coupon_app import create_app
from coupon_app.seed import seed_database

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        added = seed_database()
        print(f"Seed complete - added {added} new coupon(s).")
