from flask import Blueprint, render_template
from utils.log import logger
authentication = Blueprint("authentication", __name__)

@authentication.route("/")
def index():
    logger.info("Peticion get")
    return render_template("auth/login.html")
