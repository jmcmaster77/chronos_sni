from flask import Blueprint, redirect, url_for, render_template, request, flash, current_app
from flask_login import login_required, logout_user, UserMixin, current_user
from flask_wtf.csrf import CSRFError
from utils.log import logger, datos_log
from Services.authenticator import Autenticate
from models.Userdb import Usuarios
from utils.db import db

authentication = Blueprint("authentication", __name__)


@authentication.route("/")
def root():
    datos_request = datos_log(request)
    logger.info(datos_request)
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_page"))
    else:
        return redirect(url_for("authentication.login"))


@authentication.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        datos_request = datos_log(request)
        logger.info(datos_request)
        username = request.form["username"]
        password = request.form["password"]

        userdata = db.query(Usuarios).filter_by(username=username).first()

        if userdata != None:
            if Autenticate.login(userdata, password):
                if userdata.deleted == True:
                    logger.error(
                        "User id "
                        + str(current_user.id)
                        + " | "
                        + current_user.nombres
                        + " | "
                        + current_user.apellidos
                        + " login fallido, usuario inhabilitado"
                    )
                    flash({"title": "Chronos SNI", "message": "Usuario inhabilitado"}, "error")
                    logout_user()
                    return redirect(url_for("authentication.login"))
                else:
                    logger.info(
                        "User id "
                        + str(current_user.id)
                        + " | "
                        + current_user.nombres
                        + " | "
                        + current_user.apellidos
                        + " login exitoso"
                    )
                    flash(
                        {
                            "title": "Chronos SNI",
                            "message": "Bienvenido " + current_user.nombres + " " + current_user.apellidos,
                        },
                        "success",
                    )
                    return redirect(url_for("dashboard.dashboard_page"))
            else:
                # no puedes colocar attributos del usuarios si no esta authenticate
                logger.warning("User id " + username + " | error clave")
                flash({"title": "Chronos SNI", "message": "Error clave"}, "error")
                return redirect(url_for("authentication.login"))
        else:
            flash({"title": "Chronos SNI", "message": "Usuario " + username + " no registrado"}, "error")
            logger.error("Usuario " + username + "no registrado error login")
            return render_template("auth/login.html")

    else:

        datos_request = datos_log(request)
        logger.info(datos_request)
    return render_template("auth/login.html")


@authentication.route("/logout")
def logout():
    if current_user.is_authenticated:
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | finalizo sesión")
        current_app.config["TOASTR_CLOSE_BUTTON"] = "false"
        current_app.config["TOASTR_TIMEOUT"] = "1500"
        flash({"title": "Chronos SNI", "message": "Usuario " + current_user.username + " finaliza sesión"}, "info")
        logout_user()
        return redirect(url_for("authentication.root"))
    else:

        flash({"title": "Chronos SNI", "message": "Ningún usuario ha iniciado sesión"}, "info")

    return redirect(url_for("authentication.root"))


# Manejando errores


@authentication.errorhandler(CSRFError)
def handle_csrf_error(e):
    logger.error("CSRF token expirado: reridigiendo al login")
    flash({"title": "Chronos SNI", "message": "CSRF token expirado"}, "error")
    return redirect(url_for("authentication.login"))
