# Importar las librerias
from sqlalchemy import Column,Date, Numeric, Integer, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
import pandas as pd

# Informacion de la conexión a la base de datos de postgreSQL
USER = "selene"
PASSWORD = "12345"
HOST = "localhost"
PORT = "5432"
DB_NAME = "prueba_backup"

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Creating a Database Connection

# SQLAlchemy creates database connections using create_engine() function. This function takes a
# connection URL and returns an engine object, which manages the connection between Python and the database.


engine = create_engine(DATABASE_URL)

# Declarar la base para los modelos
Base = declarative_base()


#  Definir la clase (tabla 'prueba')
class prueba(Base):
  __tablename__ = "prueba"

  id = Column(Integer, primary_key=True, index=True)
  no_control = Column(String(20), nullable=False)
  calificacion = Column(Numeric(precision=10, scale=4))


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

#  Crear una sesión para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


#sentencia = text("SELECT * FROM prueba;")
#resultado = session.execute(sentencia)

mi_query= session.query(calificacion).filter(calificacion.materia_id == 5)
df = pd.read_sql(mi_query.statement, session.bind)

# Cerrar sesión
session.close()


#datos = pd.DataFrame(resultado.fetchall(), columns=resultado.keys())

media = df['calificacion'].astype(float).mean()
varianza = df['calificacion'].astype(float).var()
desviacion_estandar = df['calificacion'].astype(float).std()




