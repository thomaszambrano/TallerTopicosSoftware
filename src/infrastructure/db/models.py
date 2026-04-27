"""
Módulo de modelos ORM de la base de datos.

Define las clases que mapean las tablas de SQLite a objetos Python
usando SQLAlchemy. Cada modelo representa una tabla en la base de datos.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Index
from sqlalchemy.sql import func
from .database import Base


class ProductModel(Base):
    """
    Modelo ORM que representa la tabla 'products' en la base de datos.

    Almacena la información completa de cada zapato disponible en el e-commerce,
    incluyendo datos de inventario y precio.

    Attributes:
        id (int): Clave primaria autoincremental.
        name (str): Nombre del producto, máximo 200 caracteres, requerido.
        brand (str): Marca del zapato, máximo 100 caracteres.
        category (str): Categoría del zapato, máximo 100 caracteres.
        size (str): Talla del zapato, máximo 20 caracteres.
        color (str): Color del zapato, máximo 50 caracteres.
        price (float): Precio del producto en dólares.
        stock (int): Cantidad disponible en inventario.
        description (str): Descripción detallada del producto.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID único del producto")
    name = Column(String(200), nullable=False, comment="Nombre del producto")
    brand = Column(String(100), comment="Marca del zapato")
    category = Column(String(100), comment="Categoría del zapato")
    size = Column(String(20), comment="Talla del zapato")
    color = Column(String(50), comment="Color del zapato")
    price = Column(Float, comment="Precio en dólares")
    stock = Column(Integer, default=0, comment="Unidades disponibles")
    description = Column(Text, comment="Descripción detallada")

    __table_args__ = (
        Index("ix_products_brand", "brand"),
        Index("ix_products_category", "category"),
    )

    def __repr__(self) -> str:
        """Retorna representación legible del modelo para debugging."""
        return f"<ProductModel(id={self.id}, name='{self.name}', brand='{self.brand}')>"


class ChatMemoryModel(Base):
    """
    Modelo ORM que representa la tabla 'chat_memory' en la base de datos.

    Almacena el historial de conversaciones del chat, permitiendo
    mantener el contexto conversacional entre sesiones.

    Attributes:
        id (int): Clave primaria autoincremental.
        session_id (str): Identificador de la sesión de conversación, indexado.
        role (str): Rol del emisor: 'user' o 'assistant'.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje (se establece automáticamente).
    """

    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID único del mensaje")
    session_id = Column(String(100), nullable=False, comment="ID de la sesión de conversación")
    role = Column(String(20), nullable=False, comment="Rol: user o assistant")
    message = Column(Text, nullable=False, comment="Contenido del mensaje")
    timestamp = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
        comment="Fecha y hora del mensaje",
    )

    __table_args__ = (Index("ix_chat_memory_session_id", "session_id"),)

    def __repr__(self) -> str:
        """Retorna representación legible del modelo para debugging."""
        return f"<ChatMemoryModel(id={self.id}, session='{self.session_id}', role='{self.role}')>"
