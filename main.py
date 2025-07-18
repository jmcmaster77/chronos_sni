# Main Chronos Sistema de Notas Inteligente
from flask import Flask
from routes.auth import authentication
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, ipserver, soporte, config, appinfo, plantelinfo
from flask_wtf.csrf import CSRFProtect
from utils.db import engine
from schemas import Userdb
from flask_login import LoginManager
from utils.log import logger
from flask_toastr import Toastr
import sys


# Inicializando Flask
app = Flask(__name__)
# iniciando el CSRFProtect
csrf = CSRFProtect()

# Configurando toastr
toastr = Toastr()
toastr.init_app(app)

app.config['TOASTR_CLOSE_BUTTON'] = 'false'
app.config['TOASTR_TIMEOUT'] = '1500'

# Dev <- continuamos mas tarde por aca  
# Creando todas las tablas definidas en los schemas 
# Userdb.Base.metadata.create_all(bind=engine) 

# Registrando rutas en Blueprint
app.register_blueprint(authentication)

# Se carga info del usuario

# login_manager_app = LoginManager(app)
# @login_manager_app.user_loader
# def load_user(id):


if __name__ == "__main__":

    app.config.from_object(config['development'])
    csrf.init_app(app)
    logger.info("App Iniciada")
    logger.info(appinfo)
    logger.info(f"Servidor running ip:{ipserver} on port: {str(FLASK_RUN_PORT)}")
    logger.info(f"Plantel: {plantelinfo}")
    logger.info(soporte)
    mode = "produccion"
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mode = "desarrollo"

    if mode == "desarrollo":
        # Iniciar en desarrollo
        logger.info("🔧 Ejecutando en modo desarrollo")
        app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
    else:
        # Iniciar en produccion
        from waitress import serve
        logger.info("🚀 Ejecutando en modo producción con Waitress")
        serve(app, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT, threads=8)
