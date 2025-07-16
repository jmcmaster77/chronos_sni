from flask import Blueprint, render_template, request
from utils.log import logger
from user_agents import parse

authentication = Blueprint("authentication", __name__)


def datos_log(url, ip, user_agent):
    user_agent = parse(user_agent)
    navegador = user_agent.browser.family
    sistema = user_agent.os.family
    dispositivo = user_agent.device.family

    datos = (
        f"GET {url} - "
        f"IP: {ip} - "
        f"Navegador: {navegador} SO: {sistema}, Dispositivo: {dispositivo}"
    )
    return datos


@authentication.route("/")
def index():
    datos_request = datos_log(
        request.url, request.remote_addr, request.headers.get('User-Agent'))
    print(datos_request)
    logger.info(datos_request)
    return render_template("auth/login.html")
