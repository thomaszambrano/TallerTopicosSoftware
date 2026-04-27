"""
Módulo de excepciones del dominio.

Contiene excepciones específicas del negocio que representan errores
de lógica de dominio, no errores técnicos. Usar estas excepciones
en lugar de excepciones genéricas mejora la legibilidad y el manejo de errores.
"""


class ProductNotFoundError(Exception):
    """
    Excepción que se lanza cuando se intenta acceder a un producto que no existe.

    Se usa en el servicio de productos cuando se busca por ID y no se encuentra.

    Attributes:
        message (str): Mensaje descriptivo del error.

    Example:
        >>> raise ProductNotFoundError(product_id=42)
        ProductNotFoundError: Producto con ID 42 no encontrado
    """

    def __init__(self, product_id: int = None):
        """
        Inicializa la excepción con un mensaje descriptivo.

        Args:
            product_id (int, optional): ID del producto no encontrado.
                Si se proporciona, el mensaje incluye el ID específico.
        """
        if product_id is not None:
            self.message = f"Producto con ID {product_id} no encontrado"
        else:
            self.message = "Producto no encontrado"
        super().__init__(self.message)


class InvalidProductDataError(Exception):
    """
    Excepción que se lanza cuando los datos de un producto son inválidos.

    Se usa al intentar crear o actualizar un producto con datos que
    violan las reglas de negocio (precio negativo, nombre vacío, etc.).

    Attributes:
        message (str): Mensaje descriptivo indicando qué dato es inválido.

    Example:
        >>> raise InvalidProductDataError("El precio debe ser mayor a 0")
        InvalidProductDataError: El precio debe ser mayor a 0
    """

    def __init__(self, message: str = "Datos de producto inválidos"):
        """
        Inicializa la excepción con un mensaje personalizado.

        Args:
            message (str): Descripción del error de validación.
                Por defecto: 'Datos de producto inválidos'.
        """
        self.message = message
        super().__init__(self.message)


class ChatServiceError(Exception):
    """
    Excepción que se lanza cuando ocurre un error en el servicio de chat.

    Puede ser causada por fallos en la comunicación con la IA,
    errores al guardar mensajes, o problemas con el contexto conversacional.

    Attributes:
        message (str): Descripción del error ocurrido.

    Example:
        >>> raise ChatServiceError("Error al comunicarse con Gemini AI")
        ChatServiceError: Error al comunicarse con Gemini AI
    """

    def __init__(self, message: str = "Error en el servicio de chat"):
        """
        Inicializa la excepción con un mensaje descriptivo.

        Args:
            message (str): Descripción del error del servicio de chat.
                Por defecto: 'Error en el servicio de chat'.
        """
        self.message = message
        super().__init__(self.message)
