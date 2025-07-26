# Main Chronos Sistema de Notas Inteligente
from flask import Flask, request, session
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, ipserver, soporte, config, appinfo, plantelinfo
from flask_wtf.csrf import CSRFProtect
from utils.db_init import cronos_db_init
from flask_login import LoginManager
from Services.authenticator import Autenticate
from utils.log import logger
from utils.manejador_caos import status_404, status_401, csrf_error
from utils.session_refresh import latido_de_chronos
from flask_toastr import Toastr
from routes.auth import authentication
from routes.dashboard import dashboard
from routes.usuarios import usuarios
import sys, os


# Inicializando Flask
app = Flask(__name__)
# iniciando el CSRFProtect
csrf = CSRFProtect()

# Configurando toastr # la configuracion restante esta en config.py
toastr = Toastr()
toastr.init_app(app)

# Registrando rutas en Blueprint
app.register_blueprint(authentication)
app.register_blueprint(dashboard)
app.register_blueprint(usuarios)

# Se carga info del usuario

login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id):
    return Autenticate.get_by_id(id)


@app.before_request
def renovar_login_time():
    latido_de_chronos()


def mensajeria(modo):
    logger.info("App Iniciada")
    if modo == "dev":
        logger.info("🔧 Ejecutando en modo desarrollo")
    if modo == "pro":
        logger.info("🚀 Ejecutando en modo producción con Waitress")
    logger.info(appinfo)
    logger.info(f"Servidor running ip:{ipserver} on port: {str(FLASK_RUN_PORT)}")
    logger.info(f"Plantel: {plantelinfo}")
    logger.info(soporte)


if __name__ == "__main__":
    mode = "produccion"
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mode = "desarrollo"

    csrf.init_app(app)

    if mode == "desarrollo":
        # Iniciar en desarrollo
        app.config.from_object(config["development"])
        app.register_error_handler(404, status_404)
        app.register_error_handler(401, status_401)
        app.register_error_handler(400, csrf_error)

        # consulta de cositas
        # print("SQLALCHEMY_TRACK_MODIFICATIONS:", app.config.get("SQLALCHEMY_TRACK_MODIFICATIONS"))
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
            mensajeria("dev")
            # ritual de inicio de la base de datos
            cronos_db_init()

        app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
    else:
        # Iniciar en produccion
        app.config.from_object(config["produccion"])
        from waitress import serve

        mensajeria("pro")
        # ritual de inicio de la base de datos
        cronos_db_init()
        serve(app, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, threads=8)
