import pymysql
from config import hostdb, dbport, database, userdb, pwdb
from utils.log import logger
from models import Userdb
from models.Userdb import Usuarios
from utils.db import engine, db
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash


def create_database_if_not_exists():
    # Conexion al servidor Mariadb
    try:
        connection = pymysql.connect(host=hostdb, port=int(dbport), user=userdb, password=pwdb, autocommit=True)
        logger.info(f"🔄 Inicializando ritual de base de datos: {database}...")
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{database}'")
            result = cursor.fetchone()

            if not result:
                logger.info("Base de datos, no existe")
                cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                logger.info(f"✅Base de datos: {database} Creada")
                go = True
            else:
                logger.info(f"📦base de datos: {database} existe")
        connection.close()
        return True
    except Exception as e:
        logger.error(f"❌ Error al crear/verificar la base de datos: {e}")
        return False


def cronos_db_init():
    # Inicializando la base de datos
    if not create_database_if_not_exists():
        # logger.critical("🛑 Error fatal durante la creación/verificación de la base de datos. Abortando inicio.")
        logger.critical("🛑 Ritual abortado. Chronos no puede operar sin su corazón de datos.")

        sys.exit(1)
    # logger.info("✅ Base de datos lista. Continuando con el arranque del sistema...")
    creando_tablas()
    logger.info("⌛ Validando Usuarios...")
    validacion_usuarios_default()
    logger.info("🔁 Ritual completado. Chronos toma forma...")


def creando_tablas():
    logger.info("⌛ Inicializando tablas en la Base de datos...")
    Userdb.Base.metadata.create_all(bind=engine)
    logger.info("✅ Tablas inicializadas...")


def validacion_usuarios_default():
    resgistros = db.query(Usuarios).all()
    if not resgistros:
        logger.info("⌛ Crenado usuarios demo...")
        crear_usuarios("demo", "demo2025", "demo", "demo", 12345678, "admin")
        crear_usuarios("soporte", "Ryusen999*", "Jorge", "Martin", 15332813, "admin")


def crear_usuarios(username, password, nombres, apellidos, ci, rol):
    fecha = datetime.now()
    fechar = fecha.strftime("%Y/%m/%d %H:%M:%S")  # formato para el datetime en la bd
    usuario = Usuarios(username, generate_password_hash(password), nombres, apellidos, ci, rol, fechar, fechar, False)
    try:
        db.add(usuario)
        db.commit()
        db.close()
    except Exception as e:
        logger.error(e)
