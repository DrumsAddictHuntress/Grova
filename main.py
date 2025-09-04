
from config import app
from flask import render_template, redirect, url_for, jsonify
from routes_surveys import bp as surveys_bp
from routes_daily import bp as daily_bp

app.register_blueprint(surveys_bp)
app.register_blueprint(daily_bp)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/form")
def form_redirect():
    return redirect(url_for("surveys.new_survey"))

@app.route("/daily/new")
def daily_redirect():
    return redirect(url_for("daily.new_daily"))

@app.route("/report")
def report_redirect():
    return redirect(url_for("surveys.list_surveys"))


@app.route("/health", endpoint="health_check")
def health_check():
    return jsonify(status="ok"), 200

@app.route("/login", endpoint="login_stub")
def login_stub():
    return "Login coming soon", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


