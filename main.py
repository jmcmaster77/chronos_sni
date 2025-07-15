# Main Chronos Sistema de Notas Inteligente
from flask import Flask
from routes.auth import authentication
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, soporte
from flask_login import LoginManager
from utils.log import logger

# Inicializando Flask
app = Flask(__name__)

# Registrando rutas en Blueprint
app.register_blueprint(authentication)

# Se carga info del usuario  

# login_manager_app = LoginManager(app)
# @login_manager_app.user_loader
# def load_user(id):


if __name__ == "__main__":
    logger.info("App Iniciada")
    logger.info(soporte)
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
