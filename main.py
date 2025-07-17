# Main Chronos Sistema de Notas Inteligente
from flask import Flask
from routes.auth import authentication
from config import FLASK_RUN_HOST, FLASK_RUN_PORT, soporte, config
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from utils.log import logger
from flask_toastr import Toastr

# Inicializando Flask
app = Flask(__name__)
# iniciando el CSRFProtect
csrf = CSRFProtect()

# Configurando toastr 
toastr = Toastr()
toastr.init_app(app)

app.config['TOASTR_CLOSE_BUTTON'] = 'false'
app.config['TOASTR_TIMEOUT'] = '1500'


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
    logger.info(soporte)
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
