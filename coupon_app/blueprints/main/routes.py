from flask import current_app, jsonify, render_template, request
from sqlalchemy import or_

from coupon_app.blueprints.main import main_bp
from coupon_app.data import cities_by_state, states_list
from coupon_app.extensions import db
from coupon_app.models import Category, Coupon, RefreshLog
from coupon_app.services.ai import get_ai_recommendation
from coupon_app.utils import utcnow


def _active_coupons_query():
    return Coupon.query.filter(
        Coupon.is_active.is_(True),
        or_(Coupon.expires_at.is_(None), Coupon.expires_at > utcnow()),
    )


def _last_refresh():
    return RefreshLog.query.order_by(RefreshLog.ran_at.desc()).first()


@main_bp.route("/")
def home():
    coupons = [c.to_display_dict() for c in _active_coupons_query().order_by(Coupon.id).all()]
    last_refresh = _last_refresh()
    return render_template(
        "index.html",
        coupons=coupons,
        states=states_list,
        cities_by_state=cities_by_state,
        last_updated=last_refresh.ran_at if last_refresh else None,
    )


@main_bp.route("/search")
def search():
    query = request.args.get("q", "").lower()
    category = request.args.get("category", "")
    state = request.args.get("state", "")
    city = request.args.get("city", "")

    db_query = _active_coupons_query()
    if category:
        db_query = db_query.join(Category).filter(Category.name == category)

    results = []
    for coupon in db_query.order_by(Coupon.id).all():
        d = coupon.to_display_dict()
        if query and not (query in d["store"].lower() or query in d["title"].lower() or query in d["category"].lower()):
            continue
        if state and state != "All States" and not ("All" in d["states"] or state in d["states"]):
            continue
        if city and city != "All Cities" and not ("All" in d["cities"] or city in d["cities"]):
            continue
        results.append(d)

    ai_tip = None
    if query or category or city:
        # Cap the prompt size - the catalog can now grow well past the old 44 items.
        ai_tip = get_ai_recommendation(query or category or city, results[:20], current_app.config.get("GROQ_API_KEY"))

    last_refresh = _last_refresh()
    return render_template(
        "index.html",
        coupons=results,
        query=query,
        ai_tip=ai_tip,
        states=states_list,
        cities_by_state=cities_by_state,
        selected_state=state,
        selected_category=category,
        selected_city=city,
        last_updated=last_refresh.ran_at if last_refresh else None,
    )


@main_bp.route("/coupon/<int:coupon_id>")
def coupon_detail(coupon_id):
    coupon = Coupon.query.get_or_404(coupon_id)
    return render_template("coupon_detail.html", coupon=coupon.to_display_dict())


@main_bp.route("/healthz")
def healthz():
    total_coupons = _active_coupons_query().count()
    last_refresh = _last_refresh()
    return jsonify({
        "status": "ok",
        "total_coupons": total_coupons,
        "last_updated": (last_refresh.ran_at.isoformat() + "Z") if last_refresh else None,
        "version": "1.0.0",
    })
