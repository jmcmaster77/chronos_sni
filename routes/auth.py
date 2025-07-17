from flask import Blueprint, redirect, url_for,  render_template, request, flash
from utils.log import logger, datos_log


authentication = Blueprint("authentication", __name__)


@authentication.route("/")
def root():
    datos_request = datos_log(request)
    logger.info(datos_request)
    return redirect(url_for("authentication.login"))


@authentication.route("/login", methods=["GET",  "POST"])
def login():
    if request.method == "POST":
        datos_request = datos_log(request)
        logger.info(datos_request)
        username = request.form['username']
        password = request.form['password']        

        if username == "jorge" and password == "123456":
            # logger.info("User id " + str(current_user.id) + " | " + current_user.fullname + " | login")
            logger.info("User id: " + "dev" + " | " + username + " | login")
            flash({'title': "AMS", 'message': "Bienvenido " + username}, 'success')
            return render_template("dashboard.html")
        else:
            # error useer o clave 
            logger.warning("inicio de sesion fallido para el usuario: " + username + " error clave")
            flash({"title": "Chronos SNI", "message": "clave invalidad bebe"}, "error")
            return render_template("auth/login.html")

    else:

        datos_request = datos_log(request)
        logger.info(datos_request)
    return render_template("auth/login.html")
