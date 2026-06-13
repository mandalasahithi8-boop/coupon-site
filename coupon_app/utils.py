from datetime import datetime, timezone


def utcnow():
    """Naive UTC datetime - matches what SQLite stores, so comparisons stay simple."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def format_expiry(value):
    """Format a datetime back into the 'Jul 31, 2025' style the templates expect."""
    if not value:
        return "No expiry"
    return value.strftime("%b %d, %Y")
