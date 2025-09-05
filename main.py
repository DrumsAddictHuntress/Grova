from config import app, db
from flask import render_template, redirect, url_for, jsonify, flash, request
from routes_surveys import bp as surveys_bp
from routes_daily import bp as daily_bp
from auth import auth as auth_bp
from models import DailyStat, Survey
from datetime import datetime

# Register blueprints
app.register_blueprint(surveys_bp)
app.register_blueprint(daily_bp)
app.register_blueprint(auth_bp)

# Home
@app.route("/")
def home():
    return render_template("home.html")

# Survey form redirect
@app.route("/form")
def form_redirect():
    return redirect(url_for("surveys.new_survey"))

# Daily stat redirect
@app.route("/daily/new")
def daily_redirect():
    return redirect(url_for("daily.new_daily"))

# Reports landing page
@app.route("/reports")
def report_redirect():
    surveys = Survey.query.order_by(Survey.created_at.desc()).all()
    return render_template("report_list.html", surveys=surveys)

# Survey detail page (includes daily stats)
@app.route("/reports/survey/<int:survey_id>")
def report_detail(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template("report_detail.html", survey=survey)

# Survey edit
@app.route("/reports/survey/<int:survey_id>/edit", methods=["GET", "POST"])
def edit_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if request.method == "POST":
        # TODO: update survey fields
        db.session.commit()
        flash("Survey updated.", "success")
        return redirect(url_for("report_detail", survey_id=survey.id))
    return render_template("survey_edit.html", survey=survey)

# Survey delete
@app.route("/reports/survey/<int:survey_id>/delete", methods=["POST"])
def delete_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    db.session.delete(survey)
    db.session.commit()
    flash("Survey deleted.", "success")
    return redirect(url_for("report_redirect"))

# Daily stat edit
@app.route("/reports/daily/<int:stat_id>/edit", methods=["GET", "POST"])
def edit_daily(stat_id):
    stat = DailyStat.query.get_or_404(stat_id)
    if request.method == "POST":
        # TODO: update daily stat fields
        db.session.commit()
        flash("Daily stat updated.", "success")
        return redirect(url_for("report_detail", survey_id=stat.survey_id))
    return render_template("daily_edit.html", stat=stat)

# Daily stat delete
@app.route("/reports/daily/<int:stat_id>/delete", methods=["POST"])
def delete_daily(stat_id):
    stat = DailyStat.query.get_or_404(stat_id)
    survey_id = stat.survey_id
    db.session.delete(stat)
    db.session.commit()
    flash("Daily stat deleted.", "success")
    return redirect(url_for("report_detail", survey_id=survey_id))

# Health check route
@app.route("/health", endpoint="health_check")
def health_check():
    return jsonify(status="ok"), 200

# Auth pages
# Start server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

