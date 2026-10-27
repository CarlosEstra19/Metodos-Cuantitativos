from sqlalchemy import Column, Numeric, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

USER = "escuela_user"
PASSWORD = "escuela123"
HOST = "localhost"
PORT = "5432"
DB_NAME = "restaurada_db" 

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Calificacion(Base):
  __tablename__ = "calificaciones"   # <-- antes decía "cotizacion"

  id = Column(Integer, primary_key=True)
  alumno_id = Column(Integer)
  materia_id = Column(Integer)
  calificacion = Column(Numeric(5, 2))

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

mi_query = session.query(Calificacion).filter(Calificacion.materia_id == 5)
df = pd.read_sql(mi_query.statement, session.bind)

session.close()

notas = df["calificacion"].astype(float)

media = notas.mean()
varianza = notas.var()
desviacion_estandar = notas.std()


