import logging
import os

from flask import Flask, render_template

from config import config_by_name
from coupon_app.extensions import db, limiter


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["default"]))

    _configure_logging(app)
    _init_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    _init_database(app)
    _init_scheduler(app)

    return app


def _configure_logging(app):
    logging.basicConfig(
        level=app.config["LOG_LEVEL"],
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    app.logger.setLevel(app.config["LOG_LEVEL"])


def _init_extensions(app):
    db.init_app(app)
    limiter.init_app(app)


def _register_blueprints(app):
    from coupon_app.blueprints.admin import admin_bp
    from coupon_app.blueprints.api import api_bp
    from coupon_app.blueprints.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(admin_bp)


def _register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.exception("Unhandled exception")
        return render_template("500.html"), 500


def _init_database(app):
    from coupon_app.seed import seed_if_empty

    with app.app_context():
        db.create_all()
        seed_if_empty()


def _init_scheduler(app):
    if not app.config.get("SCHEDULER_ENABLED", True):
        return

    # Avoid starting a second scheduler in the Werkzeug debug reloader's parent process.
    if app.debug and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        return

    from coupon_app.services.scheduler import init_scheduler

    init_scheduler(app)
