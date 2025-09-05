# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from config import app  # uses app.config["SECRET_KEY"]

auth = Blueprint("auth", __name__)

def _serializer():
    return URLSafeTimedSerializer(app.config["SECRET_KEY"])

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm = request.form.get("confirm","")

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return render_template("signup.html")

        u = User(email=email)
        u.password_hash = generate_password_hash(password)
        db.session.add(u)
        db.session.commit()

        session.clear()
        session["user_id"] = u.id
        flash("Account created. You're now logged in.", "success")
        return redirect(url_for("home"))
    return render_template("signup.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        u = User.query.filter_by(email=email).first()
        if not u or not check_password_hash(u.password_hash, password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")
        session.clear()
        session["user_id"] = u.id
        flash("Welcome back!", "success")
        return redirect(url_for("home"))
    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        u = User.query.filter_by(email=email).first()
        if not u:
            flash("If that account exists, a reset link has been generated below.", "info")
            return render_template("forgot_password.html")
        token = _serializer().dumps({"uid": u.id})
        reset_url = url_for("auth.reset_password", token=token, _external=True)
        flash("Dev mode: use the link below to reset your password.", "info")
        return render_template("forgot_password.html", reset_url=reset_url)
    return render_template("forgot_password.html")

@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        data = _serializer().loads(token, max_age=3600)
    except SignatureExpired:
        flash("Reset link expired. Please try again.", "danger")
        return redirect(url_for("auth.forgot_password"))
    except BadSignature:
        flash("Invalid reset link.", "danger")
        return redirect(url_for("auth.forgot_password"))

    u = User.query.get(data.get("uid"))
    if not u:
        flash("User not found.", "danger")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        p1 = request.form["password"]
        p2 = request.form["confirm"]
        if p1 != p2:
            flash("Passwords do not match.", "danger")
            return render_template("reset_password.html")
        u.password_hash = generate_password_hash(p1)
        db.session.commit()
        flash("Password updated. You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html")
