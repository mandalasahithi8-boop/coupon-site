from coupon_app.extensions import db
from coupon_app.utils import format_expiry, utcnow


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    logo = db.Column(db.String(10), default="🏷️")
    url = db.Column(db.String(300), default="")

    def __repr__(self):
        return f"<Store {self.name}>"


class Coupon(db.Model):
    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    discount = db.Column(db.String(50), default="")
    url = db.Column(db.String(300), default="")
    states = db.Column(db.JSON, default=list)
    cities = db.Column(db.JSON, default=list)
    source = db.Column(db.String(50), default="seed")
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    verified = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)

    store = db.relationship("Store", backref="coupons")
    category = db.relationship("Category", backref="coupons")

    __table_args__ = (
        db.UniqueConstraint("store_id", "code", name="uq_store_code"),
    )

    def is_expired(self):
        return self.expires_at is not None and self.expires_at < utcnow()

    def to_display_dict(self):
        """Shape this row like the old hardcoded dicts so templates don't change."""
        return {
            "id": self.id,
            "store": self.store.name,
            "title": self.title,
            "code": self.code,
            "category": self.category.name,
            "discount": self.discount,
            "expires": format_expiry(self.expires_at),
            "states": self.states or ["All"],
            "cities": self.cities or ["All"],
            "url": self.url,
            "logo": self.store.logo,
        }

    def __repr__(self):
        return f"<Coupon {self.code} @ store_id={self.store_id}>"


class RefreshLog(db.Model):
    __tablename__ = "refresh_logs"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    fetched = db.Column(db.Integer, default=0)
    created = db.Column(db.Integer, default=0)
    updated = db.Column(db.Integer, default=0)
    deactivated = db.Column(db.Integer, default=0)
    duplicates_removed = db.Column(db.Integer, default=0)
    ran_at = db.Column(db.DateTime, default=utcnow, nullable=False)

    def __repr__(self):
        return f"<RefreshLog {self.source} @ {self.ran_at}>"
