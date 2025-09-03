
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from config import db
from models import Survey, DailyStat

bp = Blueprint("surveys", __name__, url_prefix="/surveys")

def _f(v):
    try: return float(v) if v not in (None, "",) else None
    except: return None

def _date(v):
    try: return datetime.strptime(v, "%Y-%m-%d").date() if v else None
    except: return None

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
            relative_humidity=_f(request.form.get("relative_humidity")),
            casing_water=_f(request.form.get("casing_water")),
            casing_bbk=_f(request.form.get("casing_bbk")),
            casing_peat_55=_f(request.form.get("casing_peat_55")),
            casing_peat_110=_f(request.form.get("casing_peat_110")),
            casing_peat_135=_f(request.form.get("casing_peat_135")),
            casing_sugar_beet_lime=_f(request.form.get("casing_sugar_beet_lime")),
            casing_hydrated_lime=_f(request.form.get("casing_hydrated_lime")),
            casing_limestone_cacho=_f(request.form.get("casing_limestone_cacho")),
            filled=request.form.get("filled","").strip() or None,
            arrived=request.form.get("arrived","").strip() or None,
            in_tunnel=request.form.get("in_tunnel","").strip() or None,
            tunnel_number=request.form.get("tunnel_number","").strip() or None,
            shipping_ph=_f(request.form.get("shipping_ph")),
            shipping_days=_f(request.form.get("shipping_days")),
            spawn_type_rate=request.form.get("spawn_type_rate","").strip() or None,
            supplement=request.form.get("supplement","").strip() or None,
            supplement_kg=_f(request.form.get("supplement_kg")),
            spawning_n=_f(request.form.get("spawning_n")),
            spawning_ash=_f(request.form.get("spawning_ash")),
            spawning_wet_weight=_f(request.form.get("spawning_wet_weight")),
            spawning_cellulose=_f(request.form.get("spawning_cellulose")),
            casing_thickness=_f(request.form.get("casing_thickness")),
            casing_ph=_f(request.form.get("casing_ph")),
            casing_humidity=_f(request.form.get("casing_humidity")),
            notes=request.form.get("notes","").strip() or None,
            is_completed=True,
        )
        if not s.room_number or not s.batch_number or s.compost_amount is None or s.compost_kg is None:
            flash("Room #, Batch #, Compost Amount and Kg are required.", "danger")
            return redirect(url_for("surveys.new_survey"))
        db.session.add(s)
        db.session.commit()
        flash("Static form saved.", "success")
        return redirect(url_for("surveys.detail", survey_id=s.id))
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to save static form: {e}", "danger")
        return redirect(url_for("surveys.new_survey"))

@bp.get("/<int:survey_id>")
def detail(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    dailies = survey.daily_stats.order_by(DailyStat.stat_date.asc()).all()
    return render_template("survey_detail.html", survey=survey, dailies=dailies)

@bp.post("/<int:survey_id>/delete")
def delete_survey(survey_id):
    s = Survey.query.get_or_404(survey_id)
    try:
        db.session.delete(s)
        db.session.commit()
        flash("Survey deleted (and its daily stats).", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to delete survey: {e}", "danger")
    return redirect(url_for("surveys.list_surveys"))

@bp.post("/<int:survey_id>/daily/<int:daily_id>/delete")
def delete_daily(survey_id, daily_id):
    d = DailyStat.query.filter_by(id=daily_id, survey_id=survey_id).first_or_404()
    try:
        db.session.delete(d)
        db.session.commit()
        flash("Daily stat deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to delete daily stat: {e}", "danger")
    return redirect(url_for("surveys.detail", survey_id=survey_id))
