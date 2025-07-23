from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user
from utils.log import logger
from utils.db import db

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html")
