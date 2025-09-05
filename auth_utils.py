
from functools import wraps
from flask import session, redirect, url_for, flash, g

def current_user_id():
    return session.get("user_id")

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped
