"""
Módulo de interfaces de repositorios del dominio.

Define los contratos que deben cumplir las implementaciones concretas
de acceso a datos. Estas interfaces permiten que el dominio sea
independiente de la base de datos o tecnología de persistencia utilizada.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interfaz que define el contrato para acceder y gestionar productos.

    Las implementaciones concretas se encuentran en la capa de infraestructura.
    Siguiendo el principio de inversión de dependencias, el dominio depende
    de esta abstracción, no de implementaciones concretas.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos registrados en el sistema.

        Returns:
            List[Product]: Lista con todos los productos. Lista vacía si no hay ninguno.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Busca un producto por su identificador único.

        Args:
            product_id (int): Identificador único del producto a buscar.

        Returns:
            Optional[Product]: El producto encontrado, o None si no existe.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene todos los productos de una marca específica.

        Args:
            brand (str): Nombre de la marca (ej. 'Nike', 'Adidas').

        Returns:
            List[Product]: Lista de productos de esa marca.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene todos los productos de una categoría específica.

        Args:
            category (str): Nombre de la categoría (ej. 'Running', 'Casual').

        Returns:
            List[Product]: Lista de productos de esa categoría.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en el sistema.

        Si el producto tiene ID, lo actualiza. Si no tiene ID, lo crea
        y asigna un ID generado automáticamente.

        Args:
            product (Product): Entidad de producto a guardar.

        Returns:
            Product: El producto guardado, con ID asignado si es nuevo.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto del sistema por su ID.

        Args:
            product_id (int): Identificador del producto a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existía.
        """
        pass


class IChatRepository(ABC):
    """
    Interfaz para gestionar el historial de conversaciones de chat.

    Permite guardar y recuperar mensajes, manteniendo la memoria
    conversacional necesaria para que la IA responda con coherencia.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje de chat en el historial.

        Args:
            message (ChatMessage): Mensaje a guardar.

        Returns:
            ChatMessage: El mensaje guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo o parcial de una sesión de chat.

        Los mensajes se retornan en orden cronológico (más antiguos primero).

        Args:
            session_id (str): Identificador de la sesión de conversación.
            limit (Optional[int]): Si se especifica, retorna solo los últimos N mensajes.

        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de mensajes de una sesión.

        Args:
            session_id (str): Identificador de la sesión a limpiar.

        Returns:
            int: Cantidad de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión de chat.

        Crucial para mantener el contexto conversacional sin sobrecargar
        la IA con mensajes demasiado antiguos.

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Número de mensajes recientes a obtener.

        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico (más antiguos primero).
        """
        pass
