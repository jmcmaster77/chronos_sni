from flask import redirect, url_for, flash, request
from flask_wtf.csrf import CSRFError
from .log import logger


def status_401(error):
    logger.error(f"Sesion expirada")
    flash({"title": "Chronos SNI", "message": "Sesion expirada"}, "error")
    return redirect(url_for("authentication.login"))


def status_404(error):
    logger.error(f"Recurso {request.url} no encontrado")
    return redirect(url_for("dashboard.error"))


def csrf_error(CSRFError):
    logger.error("CSRF token expirado: reridigiendo al login")
    flash({"title": "Chronos SNI", "message": "CSRF token expirado"}, "error")
    return redirect(url_for("authentication.login"))
