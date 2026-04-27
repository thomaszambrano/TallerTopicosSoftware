"""
Módulo de DTOs (Data Transfer Objects) de la capa de aplicación.

Los DTOs son objetos Pydantic que validan y transfieren datos entre capas.
Proveen validación automática de tipos y valores, y facilitan la
serialización/deserialización de datos en los endpoints de la API.
"""

from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos entre capas.

    Pydantic valida automáticamente los tipos y ejecuta los validadores
    personalizados al crear una instancia.

    Attributes:
        id (Optional[int]): Identificador único. None para productos nuevos.
        name (str): Nombre del producto.
        brand (str): Marca del zapato.
        category (str): Categoría del zapato.
        size (str): Talla del zapato.
        color (str): Color del zapato.
        price (float): Precio en dólares, debe ser mayor a 0.
        stock (int): Cantidad en inventario, no puede ser negativo.
        description (str): Descripción del producto.
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        """
        Valida que el precio del producto sea mayor a 0.

        Args:
            v (float): Valor del precio a validar.

        Returns:
            float: El precio validado.

        Raises:
            ValueError: Si el precio es menor o igual a 0.
        """
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v

    @field_validator("stock")
    @classmethod
    def stock_must_be_non_negative(cls, v: int) -> int:
        """
        Valida que el stock del producto no sea negativo.

        Args:
            v (int): Valor del stock a validar.

        Returns:
            int: El stock validado.

        Raises:
            ValueError: Si el stock es negativo.
        """
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v


class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir mensajes del usuario en el endpoint de chat.

    Valida que tanto el mensaje como el identificador de sesión
    sean valores no vacíos antes de procesarlos.

    Attributes:
        session_id (str): Identificador único de la sesión de conversación.
        message (str): Contenido del mensaje enviado por el usuario.
    """

    session_id: str
    message: str

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        """
        Valida que el mensaje no esté vacío o solo contenga espacios.

        Args:
            v (str): Contenido del mensaje a validar.

        Returns:
            str: El mensaje validado y sin espacios extras.

        Raises:
            ValueError: Si el mensaje está vacío.
        """
        if not v or not v.strip():
            raise ValueError("El mensaje no puede estar vacío")
        return v.strip()

    @field_validator("session_id")
    @classmethod
    def session_id_not_empty(cls, v: str) -> str:
        """
        Valida que el session_id no esté vacío.

        Args:
            v (str): Identificador de sesión a validar.

        Returns:
            str: El session_id validado y sin espacios extras.

        Raises:
            ValueError: Si el session_id está vacío.
        """
        if not v or not v.strip():
            raise ValueError("El session_id no puede estar vacío")
        return v.strip()


class ChatMessageResponseDTO(BaseModel):
    """
    DTO para enviar las respuestas del chat al cliente.

    Incluye el mensaje del usuario, la respuesta generada por la IA
    y el timestamp de la interacción.

    Attributes:
        session_id (str): Identificador de la sesión de conversación.
        user_message (str): Mensaje original del usuario.
        assistant_message (str): Respuesta generada por el asistente de IA.
        timestamp (datetime): Momento en que se procesó el mensaje.
    """

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """
    DTO para representar un mensaje individual en el historial de chat.

    Se usa al consultar el historial de conversación de una sesión.

    Attributes:
        id (int): Identificador único del mensaje.
        role (str): Rol del emisor: 'user' o 'assistant'.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    message: str
    timestamp: datetime
