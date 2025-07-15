from logging import getLogger, INFO
import logging.handlers
from concurrent_log_handler import ConcurrentRotatingFileHandler
from datetime import datetime
import os


# Configurando el registro
logger = getLogger(__name__)

# Se establece una ruta absoluta para previnr problemas con la rotacion de archivos
# Se genera un nombre para el log incluyendo año y mes
fecha = datetime.now()
filename = "Log_" + fecha.strftime('%Y%m') + ".log"
logfile = os.path.abspath(filename)

tofile = ConcurrentRotatingFileHandler(logfile, "a", 512 * 1024, 5)
tofile.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
toconsole = logging.StreamHandler()
toconsole.setLevel(logging.INFO)
toconsole.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(tofile)
logger.addHandler(toconsole)
logger.setLevel(INFO)
