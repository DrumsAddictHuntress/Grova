
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from config import db
from models import Survey, DailyStat

bp = Blueprint("daily", __name__, url_prefix="/daily")

def _f(v):
    try: return float(v) if v not in (None, "",) else None
    except: return None

def _date(v):
    try: return datetime.strptime(v, "%Y-%m-%d").date() if v else None
    except: return None

@bp.get("/new")
def new_daily():
    surveys = Survey.query.filter_by(is_completed=True).order_by(Survey.created_at.desc()).all()
    return render_template("daily_new.html", surveys=surveys)

@bp.post("")
def create_daily():
    try:
        survey_id = int(request.form["survey_id"])
        survey = Survey.query.filter_by(id=survey_id, is_completed=True).first()
        if not survey:
            flash("Please choose a valid completed form.", "danger")
            return redirect(url_for("daily.new_daily"))

        d = DailyStat(
            survey_id=survey.id,
            stat_date=_date(request.form.get("stat_date")),
            comp_ctrl=_f(request.form.get("comp_ctrl")),
            comp_temp=_f(request.form.get("comp_temp")),
            comp_max=_f(request.form.get("comp_max")),
            air_ctrl=_f(request.form.get("air_ctrl")),
            air_meas=_f(request.form.get("air_meas")),
            co2=_f(request.form.get("co2")),
            co2_meas=_f(request.form.get("co2_meas")),
            rh_meas=_f(request.form.get("rh_meas")),
            max_val=_f(request.form.get("max_val")),
            ab_val=_f(request.form.get("ab_val")),
            fresh_air=_f(request.form.get("fresh_air")),
            fresh_air_meas=_f(request.form.get("fresh_air_meas")),
            fan=_f(request.form.get("fan")),
            fan_meas=_f(request.form.get("fan_meas")),
            heat=_f(request.form.get("heat")),
            temp=_f(request.form.get("temp")),
            cool_temp=_f(request.form.get("cool_temp")),
            h2o=_f(request.form.get("h2o")),
            ref_temp=_f(request.form.get("ref_temp")),
            remarks=request.form.get("remarks","").strip() or None,
        )
        if d.stat_date is None:
            flash("Please set the Date for this daily stat.", "danger")
            return redirect(url_for("daily.new_daily"))
        db.session.add(d)
        db.session.commit()
        flash("Daily stat saved.", "success")
        return redirect(url_for("surveys.detail", survey_id=survey.id))
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to save daily stat: {e}", "danger")
        return redirect(url_for("daily.new_daily"))
