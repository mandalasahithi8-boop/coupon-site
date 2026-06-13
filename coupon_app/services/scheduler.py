import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from coupon_app.extensions import db
from coupon_app.models import RefreshLog
from coupon_app.services.ingest import cleanup_duplicates, deactivate_expired, run_full_refresh

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def init_scheduler(app):
    if scheduler.running:
        return scheduler

    def fetch_new_coupons():
        with app.app_context():
            try:
                run_full_refresh(source="scheduled_daily")
            except Exception:
                logger.exception("Daily coupon refresh job failed")

    def deactivate_expired_coupons():
        with app.app_context():
            try:
                count = deactivate_expired()
                db.session.add(RefreshLog(source="scheduled_expiry_check", deactivated=count))
                db.session.commit()
                logger.info("Expiry check deactivated %d coupon(s)", count)
            except Exception:
                logger.exception("Expiry check job failed")

    def cleanup_duplicate_coupons():
        with app.app_context():
            try:
                count = cleanup_duplicates()
                db.session.add(RefreshLog(source="scheduled_cleanup", duplicates_removed=count))
                db.session.commit()
                logger.info("Cleanup removed %d duplicate coupon(s)", count)
            except Exception:
                logger.exception("Duplicate cleanup job failed")

    # Job 1: full provider refresh, every 6 hours
    scheduler.add_job(fetch_new_coupons, IntervalTrigger(hours=6), id="daily_fetch", replace_existing=True)
    # Job 2: deactivate expired coupons, every 6 hours
    scheduler.add_job(deactivate_expired_coupons, IntervalTrigger(hours=6), id="expire_check", replace_existing=True)
    # Job 3: remove duplicate store+code coupons, weekly (Sunday 2 AM)
    scheduler.add_job(cleanup_duplicate_coupons, CronTrigger(day_of_week="sun", hour=2, minute=0), id="weekly_cleanup", replace_existing=True)

    scheduler.start()
    logger.info("Scheduler started: daily_fetch (every 6h), expire_check (every 6h), weekly_cleanup (Sun 2:00)")
    return scheduler
