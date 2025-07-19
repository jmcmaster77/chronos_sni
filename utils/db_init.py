import pymysql
from config import hostdb, dbport, database, userdb, pwdb
from utils.log import logger
import sys

def create_database_if_not_exists():
    # Conexion al servidor Mariadb 
    try:    
        connection = pymysql.connect(
            host=hostdb,
            port=int(dbport),
            user= userdb,
            password=pwdb,
            autocommit=True
        )
        logger.info(f"🔄 Inicializando ritual de base de datos: {database}...")
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{database}'")
            result = cursor.fetchone()

            if not result:
                logger.info("Base de datos, no existe")
                cursor.execute(
                    f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
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
    logger.info("🔁 Ritual completado. Chronos toma forma...")


    
    