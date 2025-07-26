from flask import Blueprint, request, redirect, url_for, render_template, flash, jsonify
from flask_login import login_required, current_user
from models.Userdb import Usuarios
from utils.db import db
from utils.log import logger, datos_log
from werkzeug.security import generate_password_hash
from datetime import datetime


usuarios = Blueprint("usuarios", __name__)


@usuarios.route("/usuarios")
@login_required
def send_usuarios():
    datos_request = datos_log(request)
    logger.info(datos_request)
    if current_user.rol == "admin":
        registros = db.query(Usuarios).all()
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | consulta usuarios")
        return render_template("mod_usuarios/usuarios.html", usuarios=registros, deleted=False)
    else:
        flash({"title": "Chronos SNI", "message": "Un administrador solo puede gestionar usuarios"}, "error")
        logger.error(
            "User id " + str(current_user.id) + " | " + current_user.username + " | intenta consultar usuarios"
        )
        return redirect(url_for("dashboard.dashboard_page"))


@usuarios.route("/usuarios_deleted")
@login_required
def send_deleted_usuarios():
    datos_request = datos_log(request)
    logger.info(datos_request)
    if current_user.rol == "admin":
        registros = db.query(Usuarios).filter_by(deleted=True).all()
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | consulta usuarios deleted")
        return render_template("mod_usuarios/usuarios.html", usuarios=registros, deleted=True)
    else:
        flash({"title": "Chronos SNI", "message": "Un administrador solo puede gestionar usuarios"}, "error")
        logger.error(
            "User id " + str(current_user.id) + " | " + current_user.username + " | intenta consultar usuarios deleted"
        )
        return redirect(url_for("dashboard.dashboard_page"))


@usuarios.route("/registraru", methods=["GET", "POST"])
@login_required
def registro_usuarios():
    datos_request = datos_log(request)
    logger.info(datos_request)
    if request.method == "GET":
        if current_user.rol == "admin":
            logger.info(
                "User id " + str(current_user.id) + " | " + current_user.username + " | ingresa al registro de usuario"
            )
            return render_template("mod_usuarios/registrou.html")
    else:
        # Validar que el nombre de usuario no este registrado
        consultaUsuario = db.query(Usuarios).filter_by(username=request.form["username"]).first()
        if consultaUsuario == None:
            # Nota: la clave y confirmacion ahora se estan validando en el front con un script antes del submit
            # validando que las claves suministradas coincidan
            fecha = datetime.now()
            fechar = fecham = fecha.strftime("%Y/%m/%d %H:%M:%S")
            new_user = Usuarios(
                request.form["username"],
                generate_password_hash(request.form["clave"]),
                request.form["nombres"],
                request.form["apellidos"],
                request.form["ci"],
                request.form["rol"],
                fechar,
                fecham,
                False,
            )
            db.add(new_user)
            db.commit()
            logger.info(
                "User id "
                + str(current_user.id)
                + " | "
                + current_user.username
                + " | Registra el usuario: "
                + new_user.username
            )
            flash(
                {
                    "title": "Chronos SNI",
                    "message": "Usuario: " + new_user.username + " registrado satisfactoriamente",
                },
                "success",
            )
            return redirect(url_for("usuarios.send_usuarios"))

        else:
            flash({"title": "Chronos SNI", "message": "El nombre de usuario ya esta en uso por otro usuario."}, "error")
            logger.error(
                "User id "
                + str(current_user.id)
                + " | "
                + current_user.username
                + " | intenta registrar usuario pero en nombre de usuario ya esta en uso"
            )
            return redirect(url_for("usuarios.registro_usuarios"))


@usuarios.route("/check-username")
@login_required
def check_username():
    username = request.args.get("username")
    exists = db.query(Usuarios).filter_by(username=username).first() is not None
    return jsonify({"exists": exists})
