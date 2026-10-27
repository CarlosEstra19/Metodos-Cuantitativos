# Importar las librerías necesarias
from sqlalchemy import Column, Numeric, Integer, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd

# Información de conexión a PostgreSQL
USER = "escuela_user"
PASSWORD = "escuela123"
HOST = "localhost"
PORT = "5432"
DB_NAME = "restaurada_db"

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Declarar la base para los modelos ORM (Sintaxis SQLAlchemy 2.0+)
Base = declarative_base()

# Definir la estructura de la tabla 'cotizacion'
class Cotizacion(Base):
    __tablename__ = "cotizacion"

    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer)
    calificacion = Column(Numeric(precision=5, scale=2))

# Crear tablas en caso de que no existan en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

try:
    # Consultar las calificaciones de la tabla cotizacion
    sentencia = text("SELECT calificacion FROM cotizacion;")
    resultado = session.execute(sentencia)

    # Cargar los registros en un DataFrame de Pandas
    datos = pd.DataFrame(resultado.fetchall(), columns=resultado.keys())

    if not datos.empty:
        # Convertir a float para poder realizar operaciones matemáticas
        columna = datos['calificacion'].astype(float)

        # Calcular únicamente las métricas solicitadas
        media = columna.mean()
        varianza = columna.var()
        desviacion_estandar = columna.std()

        # Imprimir resultados
        print(f"Media: {media:.2f}")
        print(f"Varianza: {varianza:.2f}")
        print(f"Desviación Estándar: {desviacion_estandar:.2f}")
    else:
        print("La tabla 'cotizacion' no contiene registros.")

finally:
    # Cerrar siempre la sesión de la base de datos
    session.close()
