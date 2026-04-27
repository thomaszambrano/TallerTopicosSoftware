"""
Módulo de configuración de la base de datos.

Configura SQLAlchemy para usar SQLite como motor de base de datos.
Proporciona la sesión de base de datos y funciones de inicialización.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ...config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Genera una sesión de base de datos para ser usada como dependencia en FastAPI.

    Utiliza el patrón yield para garantizar que la sesión se cierre
    correctamente después de cada request, incluso si ocurre un error.

    Yields:
        Session: Sesión activa de SQLAlchemy para interactuar con la base de datos.

    Example:
        >>> @app.get("/items")
        ... def get_items(db: Session = Depends(get_db)):
        ...     return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos ORM.

    Debe ejecutarse al arrancar la aplicación. Crea las tablas si no existen
    y luego carga los datos iniciales de productos si la base de datos está vacía.

    Note:
        Esta función es idempotente: si las tablas ya existen, no las modifica.
        Se importa aquí para evitar importaciones circulares.

    Returns:
        None
    """
    from .models import ProductModel, ChatMemoryModel  # noqa: F401
    from .init_data import load_initial_data

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        load_initial_data(db)
    finally:
        db.close()
