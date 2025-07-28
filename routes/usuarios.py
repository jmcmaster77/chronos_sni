from flask import Blueprint, request, redirect, url_for, render_template, flash, jsonify
from flask_login import login_required, current_user
from models.Userdb import Usuarios
from utils.db import db
from utils.log import logger, datos_log
from werkzeug.security import generate_password_hash
from datetime import datetime


usuarios = Blueprint("usuarios", __name__)


# validacion si el usario tiene privilegios para el modulo de usuarios #tambien evita que ingrese a las endpoint manualmente
def isadmin(user):
    if user.rol != "admin":
        flash({"title": "Chronos SNI", "message": "Un administrador solo puede gestionar usuarios"}, "error")
        logger.error("User id " + str(user.id) + " | " + user.username + " | intenta acceder al modulo usuarios")
        return False
    else:
        return True


@usuarios.route("/usuarios")
@login_required
def send_usuarios():
    datos_request = datos_log(request)
    logger.info(datos_request)

    if isadmin(current_user):
        print("rico")
        registros = db.query(Usuarios).all()
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | consulta usuarios")
        return render_template("mod_usuarios/usuarios.html", usuarios=registros, deleted=False)
    else:
        return redirect(url_for("dashboard.dashboard_page"))


@usuarios.route("/usuarios_deleted")
@login_required
def send_deleted_usuarios():
    datos_request = datos_log(request)
    logger.info(datos_request)
    if isadmin(current_user):
        registros = db.query(Usuarios).filter_by(deleted=True).all()
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | consulta usuarios deleted")
        return render_template("mod_usuarios/usuarios.html", usuarios=registros, deleted=True)
    else:
        return redirect(url_for("dashboard.dashboard_page"))


@usuarios.route("/registraru", methods=["GET", "POST"])
@login_required
def registro_usuarios():
    datos_request = datos_log(request)
    logger.info(datos_request)
    if request.method == "GET":
        if isadmin(current_user):
            logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | ingresa al registro de usuario")
            return render_template("mod_usuarios/registrou.html")
        else:
            return redirect(url_for("dashboard.dashboard_page"))

    else:

        # Nota: la clave y confirmacion ahora se estan validando en el front con un script antes del submit
        # la validacion del username no este en uso esta validad antes del submit con una consulta al endpoint check_username
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
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | Registra el usuario: " + new_user.username)
        mensaje = f"Usuario: " + new_user.username + " registrado satisfactoriamente"
        flash({"title": "Chronos SNI", "message": mensaje}, "success")
        return redirect(url_for("usuarios.send_usuarios"))


@usuarios.route("/check-username")
@login_required
def check_username():
    username = request.args.get("username")
    exists = db.query(Usuarios).filter_by(username=username).first() is not None
    return jsonify({"exists": exists})


@usuarios.route("/check-username-mod")
@login_required
def check_username_mod():
    username = request.args.get("username")
    id = request.args.get("id")
    exists = db.query(Usuarios).filter(Usuarios.username == username, Usuarios.id != id).first() is not None
    return jsonify({"exists": exists})


def validacion_usuario_soporte(id, current_user_id):
    # El id 2 solo pueda ser modificado por el mismo
    if id == "2" and current_user_id == 2:
        return True
    elif id == "2" and current_user_id != 2:
        return False
    else:
        return True


@usuarios.route("/modificar_user/<id>", methods=["GET", "POST"])
@login_required
def modificar_user(id):
    datos_request = datos_log(request)
    logger.info(datos_request)
    if request.method == "GET":
        if isadmin(current_user):
            logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | ingresa a modificacion de usuario")
            userdata = db.get(Usuarios, id)
            if validacion_usuario_soporte(id, current_user.id):
                return render_template("mod_usuarios/modificaru.html", userdata=userdata)
            else:
                mensaje = f"El usuario:  {userdata.username}  no puede ser modificado"
                flash({"title": "Chronos SNI", "message": mensaje}, "error")
            return redirect(url_for("usuarios.send_usuarios"))
        else:

            return redirect(url_for("dashboard.dashboard_page"))
    else:

        userdata = db.get(Usuarios, id)
        userdata.username = request.form["username"]
        userdata.nombres = request.form["nombres"]
        userdata.apellidos = request.form["apellidos"]
        userdata.ci = request.form["ci"]
        if id == "2":
            rol = "admin"
        else:
            rol = request.form["rol"]
        userdata.rol = rol
        fecham = datetime.now()
        userdata.fecham = fecham.strftime("%Y/%m/%d %H:%M:%S")
        db.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | modifica usuario: " + str(userdata.id))
        mensaje = f"Usuario: {current_user.username} modifico el usuario id {str(userdata.id)}"
        flash({"title": "Chronos SNI", "message": mensaje}, "success")
        return redirect(url_for("usuarios.send_usuarios"))


@usuarios.route("/borraru/<id>")
@login_required
def borraru(id):
    datos_request = datos_log(request)
    logger.info(datos_request)
    if isadmin(current_user):

        userdata = db.get(Usuarios, id)
        if id == "2":
            mensaje = f"El usuario:  {userdata.username}  no puede ser marcado como borrado"
            flash({"title": "Chronos SNI", "message": mensaje}, "warning")
            return redirect(url_for("usuarios.send_usuarios"))
        else:
            fecha = datetime.now()
            userdata.fecham = fecha.strftime("%Y/%m/%d %H:%M:%S")
            userdata.deleted = True
            db.commit()
            logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | Marca id: " + id + ", como borrado")
            mensaje = f"El usuario:  {userdata.username} fue marcado como borrado"
            flash({"title": "Chronos SNI", "message": mensaje}, "success")

            return redirect(url_for("usuarios.send_usuarios"))
    else:

        return redirect(url_for("dashboard.dashboard_page"))


@usuarios.route("/restauraru/<id>")
@login_required
def restauraru(id):
    datos_request = datos_log(request)
    logger.info(datos_request)
    if isadmin(current_user):
        userdata = db.get(Usuarios, id)
        fecha = datetime.now()
        userdata.fecham = fecha.strftime("%Y/%m/%d %H:%M:%S")
        userdata.deleted = False
        db.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | Restaura el id: " + id)
        mensaje = f"El usuario:  {userdata.username} fue restaurado"
        flash({"title": "Chronos SNI", "message": mensaje}, "success")

        return redirect(url_for("usuarios.send_usuarios"))
    else:

        return redirect(url_for("dashboard.dashboard_page"))


@usuarios.route("/eliminaru/<id>")
@login_required
def eliminaru(id):
    datos_request = datos_log(request)
    logger.info(datos_request)
    if isadmin(current_user):
        userdata = db.get(Usuarios, id)

        if id == "2":
            mensaje = f"El usuario:  {userdata.username}  no puede ser eliminado"
            flash({"title": "Chronos SNI", "message": mensaje}, "warning")
            return redirect(url_for("usuarios.send_usuarios"))

        db.deleted
        db.commit()
        logger.info("User id " + str(current_user.id) + " | " + current_user.username + " | elimina el id: " + id)
        mensaje = f"El usuario:  {userdata.username} fue eliminado"
        flash({"title": "Chronos SNI", "message": mensaje}, "success")

        return redirect(url_for("usuarios.send_usuarios"))
    else:

        return redirect(url_for("dashboard.dashboard_page"))
