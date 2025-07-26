from flask import request, session
from datetime import datetime
import pytz


def latido_de_chronos():
    # rutas excluidas
    rutas_excluidas = ["login", "static"]
    if request.endpoint and request.endpoint not in rutas_excluidas:
        caracas_tz = pytz.timezone("America/Caracas")
        session["login_time"] = datetime.now(caracas_tz).isoformat()
