from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from config import conexuridb

engine = create_engine(conexuridb)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
db: Session = SessionLocal()