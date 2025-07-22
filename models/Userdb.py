from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from utils.db import engine

Base = declarative_base()


class Usuarios(Base):
    __tablename__ = "Usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    ci = Column(Integer, nullable=False)
    rol = Column(String(10))
    fechar = Column(DateTime)
    fecham = Column(DateTime)
    deleted = Column(Boolean)

    def __init__(self, username, password, nombres, apellidos, ci, rol, fechar, fecham, deleted):
        self.username = username
        self.password = password
        self.nombres = nombres
        self.apellidos = apellidos
        self.ci = ci
        self.rol = rol
        self.fechar = fechar
        self.fecham = fecham
        self.deleted = deleted
