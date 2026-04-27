"""
Módulo del servicio de aplicación para el chat con IA.

Orquesta la interacción entre el repositorio de productos, el repositorio
de chat y el servicio de Gemini AI para proporcionar respuestas contextuales
y coherentes a los usuarios del e-commerce.
"""

from typing import List, Optional
from datetime import datetime, timezone
from ..domain.entities import ChatMessage, ChatContext
from ..domain.repositories import IProductRepository, IChatRepository
from ..domain.exceptions import ChatServiceError
from .dtos import ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO


class ChatService:
    """
    Servicio de aplicación para gestionar el chat conversacional con IA.

    Coordina el flujo completo de una conversación: obtiene el contexto,
    genera respuestas con Gemini AI y persiste el historial.

    Attributes:
        product_repo (IProductRepository): Repositorio de productos para consultar inventario.
        chat_repo (IChatRepository): Repositorio de mensajes para persistir el historial.
        ai_service: Servicio de IA (GeminiService) para generar respuestas.
    """

    def __init__(
        self,
        product_repo: IProductRepository,
        chat_repo: IChatRepository,
        ai_service,
    ):
        """
        Inicializa el servicio con las dependencias necesarias.

        Args:
            product_repo (IProductRepository): Repositorio de productos.
            chat_repo (IChatRepository): Repositorio de mensajes de chat.
            ai_service: Instancia del servicio de IA (GeminiService).
        """
        self.product_repo = product_repo
        self.chat_repo = chat_repo
        self.ai_service = ai_service

    async def process_message(
        self, request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta con IA.

        Flujo completo:
        1. Obtiene los productos disponibles del repositorio.
        2. Recupera los últimos 6 mensajes del historial de la sesión.
        3. Crea un ChatContext con el historial.
        4. Llama al servicio de IA con el mensaje, productos y contexto.
        5. Guarda el mensaje del usuario y la respuesta en el repositorio.
        6. Retorna el DTO con la respuesta.

        Args:
            request (ChatMessageRequestDTO): Datos del mensaje del usuario.

        Returns:
            ChatMessageResponseDTO: Respuesta generada con mensaje del usuario,
                respuesta de la IA y timestamp.

        Raises:
            ChatServiceError: Si ocurre un error al procesar el mensaje o
                comunicarse con el servicio de IA.

        Example:
            >>> request = ChatMessageRequestDTO(
            ...     session_id="usuario_001",
            ...     message="Busco zapatos Nike para correr"
            ... )
            >>> response = await chat_service.process_message(request)
            >>> print(response.assistant_message)
            "Tengo varias opciones Nike para running..."
        """
        try:
            products = self.product_repo.get_all()
            recent_messages = self.chat_repo.get_recent_messages(
                request.session_id, count=6
            )
            context = ChatContext(messages=recent_messages)
            assistant_response = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context,
            )
            timestamp = datetime.now(timezone.utc)
            user_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=timestamp,
            )
            assistant_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_response,
                timestamp=timestamp,
            )
            self.chat_repo.save_message(user_msg)
            self.chat_repo.save_message(assistant_msg)
            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_response,
                timestamp=timestamp,
            )
        except ChatServiceError:
            raise
        except Exception as e:
            raise ChatServiceError(f"Error al procesar el mensaje: {str(e)}")

    def get_session_history(
        self, session_id: str, limit: Optional[int] = 10
    ) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial de conversación de una sesión.

        Args:
            session_id (str): Identificador de la sesión.
            limit (Optional[int]): Número máximo de mensajes a retornar. Por defecto 10.

        Returns:
            List[ChatHistoryDTO]: Lista de mensajes del historial como DTOs.
        """
        messages = self.chat_repo.get_session_history(session_id, limit=limit)
        return [
            ChatHistoryDTO(
                id=msg.id,
                role=msg.role,
                message=msg.message,
                timestamp=msg.timestamp,
            )
            for msg in messages
        ]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina el historial completo de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión a limpiar.

        Returns:
            int: Número de mensajes eliminados.
        """
        return self.chat_repo.delete_session_history(session_id)
