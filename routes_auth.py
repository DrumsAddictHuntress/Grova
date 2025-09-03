
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user
from email_validator import validate_email, EmailNotValidError
from config import app, db
from models import User

bp = Blueprint("auth", __name__, url_prefix="")

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Welcome back!", "success")
            next_url = request.args.get("next") or url_for("home")
            return redirect(next_url)
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@bp.route("/signup", methods=["GET","POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        confirm = request.form.get("confirm") or ""
        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash("Please enter a valid email address.", "danger")
            return render_template("signup.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("signup.html")
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("signup.html")
        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "warning")
            return redirect(url_for("login"))
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Account created. You can log in now.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@bp.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.get_reset_token()
            reset_url = url_for("reset_password", token=token, _external=True)
            # In production, send email. Here, just flash the link.
            flash(f"Password reset link: {reset_url}", "info")
        else:
            flash("If that email exists, a reset link has been sent.", "info")
        return redirect(url_for("login"))
    return render_template("forgot.html")

@bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash("Invalid or expired reset token.", "danger")
        return redirect(url_for("forgot_password"))
    if request.method == "POST":
        password = request.form.get("password") or ""
        confirm = request.form.get("confirm") or ""
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("reset.html")
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("reset.html")
        user.set_password(password)
        db.session.commit()
        flash("Password has been reset. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("reset.html")
