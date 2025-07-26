from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app
from flask_login import login_required, current_user
from utils.log import logger, datos_log
from utils.db import db


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def dashboard_page():
    datos_request = datos_log(request)
    logger.info(datos_request)
    # ================= Reaudacion datos para el dash Board
    # ya veremos que se va a pintar

    logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | llega al dashboard")
    return render_template("dashboard.html")


@dashboard.route("/acercade")
@login_required
def acercade():
    datos_request = datos_log(request)
    logger.info(datos_request)
    logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | consulta acercade")
    return render_template("acerca.html")


@dashboard.route("/error")
@login_required
def error():
    datos_request = datos_log(request)
    logger.info(datos_request)
    flash({"title": "Chronos SNI", "message": "Recurso no encontrado"}, "error")
    logger.error("User id " + str(current_user.id) + " | " + current_user.username + " | ingresa a ruta inexistente")
    return render_template("error.html")
