from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user
from utils.log import logger
from utils.db import db

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_page():
    # ================= Reaudacion datos para el dash Board
    # ya veremos que se va a pintar 

    

    return render_template("dashboard.html")


@dashboard.route("/acercade")
@login_required
def acercade():
    return render_template("acerca.html")


@dashboard.route("/error")
@login_required
def error():
    flash({"title": "Chronos SNI", "message": "Recurso no encontrado"}, "error")
    return render_template("error.html")
