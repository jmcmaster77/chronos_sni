from dotenv import load_dotenv
import os

load_dotenv()

hostdb = os.environ["dbhost"]
dbport = os.environ["dbport"]
database = os.environ["database"]
userdb = os.environ["userdb"]
pwdb = os.environ["pwdb"]
sk = os.environ["sk"]
FLASK_RUN_HOST = os.environ["FLASK_RUN_HOST"]
FLASK_RUN_PORT = os.environ["FLASK_RUN_PORT"]
ipserver = os.environ["IPSERVER"]
appinfo = os.environ["appinfo"]
plantelinfo = os.environ["plantelinfo"] 
soporte = os.environ["soporte"]

conexuridb = f"mariadb+pymysql://{userdb}:{pwdb}@{hostdb}:{dbport}/{database}?charset=utf8mb4"

class Config:
    SECRET_KEY = sk


class DevelomentConfig(Config):
    DEBUG = True


config = {
    "development": DevelomentConfig
}
