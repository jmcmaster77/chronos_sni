from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from models.Userdb import Usuarios
from utils.db import db
from utils.log import logger
from werkzeug.security import generate_password_hash

usuarios = Blueprint("usuarios", __name__)


@usuarios.route("/usuarios")
@login_required
def mod_usuarios():
    if current_user.rol == "admin":
        registros = db.query(Usuarios).all()
        if registros is not None:
            for registro in registros:
                registro.fechar = registro.fechar.strftime("%d/%m/%y %H:%M")
                registro.fecham = registro.fecham.strftime("%d/%m/%y %H:%M")

            return render_template("mod_usuarios/usuarios.html", usuarios=registros, deleted=False)
        else:
            return render_template("mod_usuarios/usuarios.html", usuarios=registros, deleted=False)
    else:
        flash({"title": "Chronos SNI", "message": "Un administrador solo puede gestionar usuarios"}, "error")
        return redirect(url_for("dashboard.dashboard_page"))
