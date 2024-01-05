from flask import Blueprint, render_template
from flask_login import login_required

from src.lib.auth_checks import check_is_confirmed

dashboardBp = Blueprint("dashboard", __name__)

@dashboardBp.route("/")
@login_required
@check_is_confirmed
def home():
    return render_template("dashboard/index.html")

@dashboardBp.route("/profile")
@login_required
@check_is_confirmed
def profile():
    return render_template("dashboard/profile.html")