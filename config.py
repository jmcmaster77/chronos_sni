from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ["host"]
database = os.environ["database"]
userdb = os.environ["user"]
passworddb = os.environ["password"]
portdb = os.environ["port"]
ks = os.environ["ks"]
FLASK_RUN_HOST = os.environ["FLASK_RUN_HOST"]
FLASK_RUN_PORT = os.environ["FLASK_RUN_PORT"]
soporte = os.environ["soporte"]


class Config:
    SECRET_KEY = ks


class DevelomentConfig(Config):
    DEBUG = True


config = {
    "development": DevelomentConfig
}
