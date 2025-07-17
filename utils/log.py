from logging import getLogger, INFO
import logging.handlers
from concurrent_log_handler import ConcurrentRotatingFileHandler
from datetime import datetime
from user_agents import parse
import os


# Configurando el registro
logger = getLogger(__name__)

# Se establece una ruta absoluta para previnr problemas con la rotacion de archivos
# Se genera un nombre para el log incluyendo año y mes
fecha = datetime.now()
filename = "Log_" + fecha.strftime('%Y%m') + ".log"
logfile = os.path.abspath(filename)

tofile = ConcurrentRotatingFileHandler(logfile, "a", 512 * 1024, 5)
tofile.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
toconsole = logging.StreamHandler()
toconsole.setLevel(logging.INFO)
toconsole.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(tofile)
logger.addHandler(toconsole)
logger.setLevel(INFO)


# funciones de apoyo para dar formato a los input al log de las peticiones get

def datos_log(request):
    user_agent = parse(request.headers.get('User-Agent', 'Desconocido'))
    navegador = user_agent.browser.family
    sistema = user_agent.os.family
    dispositivo = user_agent.device.family
    # de requerir informacion de parametros se puede incluir un campo payload con estos pero 
    # hay que validar el metodo de la peticion get request.args o put request.form <- pasarlo a dict 
    
    datos = (
        f"{request.method} - {request.url} - "
        f"IP: {request.remote_addr} - "
        f"Navegador: {navegador} SO: {sistema}, Dispositivo: {dispositivo}"
    )
    return datos
