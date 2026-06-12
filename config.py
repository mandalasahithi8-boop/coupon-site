import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


def _normalize_db_uri(uri):
    # Render/Heroku-style URLs use "postgres://"; SQLAlchemy 1.4+ needs "postgresql://"
    if uri and uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql://", 1)
    return uri


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    SQLALCHEMY_DATABASE_URI = _normalize_db_uri(
        os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(INSTANCE_DIR, "coupons.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Admin endpoint for manually triggering a coupon refresh.
    ADMIN_REFRESH_TOKEN = os.environ.get("ADMIN_REFRESH_TOKEN")

    # Optional comma-separated list of RSS feed URLs to scrape for deals.
    RSS_FEED_URLS = os.environ.get("RSS_FEED_URLS")

    SCHEDULER_ENABLED = os.environ.get("SCHEDULER_ENABLED", "true").lower() == "true"


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SCHEDULER_ENABLED = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
