from flask import jsonify

from coupon_app.blueprints.api import api_bp


@api_bp.route("/ping")
def ping():
    return jsonify({"status": "ok"})
