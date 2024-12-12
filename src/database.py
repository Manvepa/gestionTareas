from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Crear motor de base de datos con la opción 'check_same_thread=False'
engine = create_engine('sqlite:///data/tasks.db', connect_args={'check_same_thread': False})

# Crear todas las tablas
Base.metadata.create_all(engine)

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()
