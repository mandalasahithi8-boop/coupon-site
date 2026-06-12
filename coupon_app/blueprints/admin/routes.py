import secrets

from flask import current_app, jsonify, request

from coupon_app.blueprints.admin import admin_bp
from coupon_app.extensions import limiter
from coupon_app.services.ingest import run_full_refresh


def _is_authorized():
    expected = current_app.config.get("ADMIN_REFRESH_TOKEN")
    if not expected:
        return False
    provided = request.headers.get("X-Admin-Token") or request.args.get("token", "")
    return secrets.compare_digest(provided, expected)


@admin_bp.route("/refresh", methods=["POST"])
@limiter.limit("5 per hour")
def refresh():
    if not _is_authorized():
        return jsonify({"error": "unauthorized"}), 401

    result = run_full_refresh(source="manual")
    return jsonify({"status": "ok", **result})
