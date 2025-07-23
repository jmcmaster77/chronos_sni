from models.entities.UserEntity import User
from models.Userdb import Usuarios
from flask_login import login_user
from utils.db import db


class Autenticate:
    @classmethod
    def login(self, userdata, password):
        try:
            # consulta usuario en la db

            if User.check_password(userdata.password, password):
                user = User(userdata.id, userdata.username, None, userdata.nombres, userdata.apellidos, userdata.rol)
                login_user(user)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(e)

    @classmethod
    def get_by_id(self, id):
        try:
            userdata = db.get(Usuarios, id)
            if userdata != None:
                user = User(userdata.id, userdata.username, None, userdata.nombres, userdata.apellidos, userdata.rol)
                return user
            else:
                return None
        except Exception as e:
            raise Exception(e)
