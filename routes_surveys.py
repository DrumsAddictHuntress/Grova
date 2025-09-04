
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from config import db
from models import Survey, DailyStat

bp = Blueprint("surveys", __name__, url_prefix="/surveys")

# Safer float parser: tolerate blanks and comma decimals
def _f(v):
    try:
        if v is None or v == "":
            return None
        v = v.replace(",", ".")
        return float(v)
    except Exception:
        return None

def _date(v):
    try:
        return datetime.strptime(v, "%Y-%m-%d").date() if v else None
    except:
        return None

@bp.get("")
def list_surveys():
    surveys = Survey.query.order_by(Survey.created_at.desc()).all()
    return render_template("survey_list.html", surveys=surveys)

@bp.get("/new")
def new_survey():
    return render_template("survey_form.html")

@bp.post("")
def create_survey():
    try:
        s = Survey(
            room_number=request.form.get("room_number","").strip(),
            batch_number=request.form.get("batch_number","").strip(),
            filling_date=_date(request.form.get("filling_date")),
            compost_amount=_f(request.form.get("compost_amount")),
            compost_kg=_f(request.form.get("compost_kg")),
            missing_section=request.form.get("missing_section","").strip() or None,
            total_room_m2=_f(request.form.get("total_room_m2")),
            extra_compost=_f(request.form.get("extra_compost")),
            compost_remarks=request.form.get("compost_remarks","").strip() or None,
            compost_arrival=request.form.get("compost_arrival","").strip() or None,
            compost_camion_temp=_f(request.form.get("compost_camion_temp")),
            extra_water=_f(request.form.get("extra_water")),
            compost_height=_f(request.form.get("compost_height")),
            compost_moist=_f(request.form.get("compost_moist")),
            compost_length=_f(request.form.get("compost_length")),
            compost_texture=_f(request.form.get("compost_texture")),
            compost_spawn=_f(request.form.get("compost_spawn")),
            relative_humidity=_f(request.form.get("relative_humidity"))
        )
        db.session.add(s)
        db.session.commit()
        flash("Static form saved.", "success")
        return redirect(url_for("surveys.list_surveys"))
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to save static form: {e}", "danger")
        return redirect(url_for("surveys.new_survey"))
