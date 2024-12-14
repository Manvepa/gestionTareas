from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

# Crear motor de base de datos con la opción 'check_same_thread=False'
# Usamos SQLite en memoria para pruebas
engine = create_engine('sqlite:///data/tasks.db', connect_args={'check_same_thread': False})

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear una sesión de ámbito de subproceso
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

# Proveer la sesión
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
