"""
Módulo de entidades del dominio.

Contiene las entidades principales del negocio: Product, ChatMessage y ChatContext.
Estas clases son el núcleo de la aplicación y no dependen de ningún framework externo.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """
    Entidad que representa un producto (zapato) en el e-commerce.

    Contiene la lógica de negocio relacionada con productos,
    incluyendo validaciones de precio, stock y disponibilidad.

    Attributes:
        id (Optional[int]): Identificador único del producto. None si es nuevo.
        name (str): Nombre del producto, no puede estar vacío.
        brand (str): Marca del zapato (Nike, Adidas, Puma, etc.).
        category (str): Categoría del zapato (Running, Casual, Formal).
        size (str): Talla del zapato.
        color (str): Color del zapato.
        price (float): Precio en dólares, debe ser mayor a 0.
        stock (int): Cantidad disponible en inventario, no puede ser negativo.
        description (str): Descripción detallada del producto.
    """

    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Ejecuta validaciones de negocio después de crear el objeto.

        Raises:
            ValueError: Si el precio es menor o igual a 0.
            ValueError: Si el stock es negativo.
            ValueError: Si el nombre está vacío.
        """
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacío")

    def is_available(self) -> bool:
        """
        Verifica si el producto tiene stock disponible para ser vendido.

        Returns:
            bool: True si el stock es mayor a 0, False en caso contrario.

        Example:
            >>> product = Product(id=1, name="Nike Air", brand="Nike",
            ...     category="Running", size="42", color="Negro",
            ...     price=120.0, stock=5, description="Zapato running")
            >>> product.is_available()
            True
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto en la cantidad especificada.

        Se usa típicamente al realizar una venta. Valida que haya
        suficiente stock antes de reducir.

        Args:
            quantity (int): Cantidad a reducir del stock. Debe ser positivo.

        Raises:
            ValueError: Si quantity es menor o igual a 0.
            ValueError: Si la cantidad supera el stock disponible.

        Example:
            >>> product.reduce_stock(3)
            >>> print(product.stock)
            2
        """
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser positiva")
        if quantity > self.stock:
            raise ValueError(
                f"Stock insuficiente. Disponible: {self.stock}, solicitado: {quantity}"
            )
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto en la cantidad especificada.

        Se usa al recibir nuevas unidades del producto.

        Args:
            quantity (int): Cantidad a agregar al stock. Debe ser positivo.

        Raises:
            ValueError: Si quantity es menor o igual a 0.

        Example:
            >>> product.increase_stock(10)
            >>> print(product.stock)
            15
        """
        if quantity <= 0:
            raise ValueError("La cantidad a agregar debe ser positiva")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en la conversación de chat.

    Cada mensaje pertenece a una sesión y tiene un rol que indica
    si fue enviado por el usuario o por el asistente de IA.

    Attributes:
        id (Optional[int]): Identificador único del mensaje.
        session_id (str): Identificador de la sesión de conversación.
        role (str): Rol del emisor: 'user' para el usuario o 'assistant' para la IA.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora en que se envió el mensaje.
    """

    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self):
        """
        Ejecuta validaciones de negocio después de crear el objeto.

        Raises:
            ValueError: Si el role no es 'user' ni 'assistant'.
            ValueError: Si el mensaje está vacío.
            ValueError: Si el session_id está vacío.
        """
        if self.role not in ("user", "assistant"):
            raise ValueError("El role debe ser 'user' o 'assistant'")
        if not self.message or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacío")
        if not self.session_id or not self.session_id.strip():
            raise ValueError("El session_id no puede estar vacío")

    def is_from_user(self) -> bool:
        """
        Verifica si el mensaje fue enviado por el usuario.

        Returns:
            bool: True si el role es 'user', False en caso contrario.
        """
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """
        Verifica si el mensaje fue enviado por el asistente de IA.

        Returns:
            bool: True si el role es 'assistant', False en caso contrario.
        """
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.

    Mantiene los mensajes recientes para dar coherencia al chat con IA.
    Permite que el asistente recuerde el hilo de la conversación.

    Attributes:
        messages (list[ChatMessage]): Lista de mensajes de la conversación.
        max_messages (int): Número máximo de mensajes recientes a considerar.
            Por defecto 6.
    """

    messages: list
    max_messages: int = 6

    def get_recent_messages(self) -> list:
        """
        Retorna los últimos N mensajes según max_messages.

        Usa slicing para obtener solo los mensajes más recientes,
        lo que limita el contexto enviado a la IA y reduce costos.

        Returns:
            list[ChatMessage]: Lista con los últimos max_messages mensajes.

        Example:
            >>> context = ChatContext(messages=[msg1, msg2, msg3, msg4, msg5, msg6, msg7])
            >>> recent = context.get_recent_messages()
            >>> len(recent)
            6
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes recientes para incluirlos en el prompt de la IA.

        Construye un string con el historial de conversación en formato
        legible para el modelo de lenguaje.

        Returns:
            str: Historial formateado con prefijos 'Usuario:' y 'Asistente:'.
                Retorna string vacío si no hay mensajes.

        Example:
            >>> context.format_for_prompt()
            'Usuario: Busco zapatos Nike\\nAsistente: Tenemos varios modelos...'
        """
        recent = self.get_recent_messages()
        if not recent:
            return ""
        lines = []
        for msg in recent:
            prefix = "Usuario" if msg.is_from_user() else "Asistente"
            lines.append(f"{prefix}: {msg.message}")
        return "\n".join(lines)
