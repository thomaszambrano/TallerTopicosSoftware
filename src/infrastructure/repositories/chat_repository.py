"""
Módulo del repositorio concreto de mensajes de chat.

Implementa la interfaz IChatRepository usando SQLAlchemy y SQLite.
Gestiona la persistencia del historial de conversaciones.
"""

from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ...domain.entities import ChatMessage
from ...domain.repositories import IChatRepository
from ..db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """
    Implementación concreta del repositorio de chat usando SQLAlchemy.

    Gestiona la persistencia y recuperación de mensajes del historial
    de conversaciones entre usuarios y el asistente de IA.

    Attributes:
        db (Session): Sesión activa de SQLAlchemy inyectada en el constructor.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con la sesión de base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy para ejecutar queries.
        """
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje de chat en la base de datos.

        Args:
            message (ChatMessage): Entidad de mensaje a persistir.

        Returns:
            ChatMessage: El mensaje guardado con su ID asignado por la base de datos.
        """
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial de mensajes de una sesión.

        Los mensajes se retornan en orden cronológico (más antiguos primero).
        Si se especifica limit, retorna solo los últimos N mensajes.

        Args:
            session_id (str): Identificador de la sesión de conversación.
            limit (Optional[int]): Si se especifica, retorna solo los últimos N mensajes.

        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        query = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.asc())
        )
        if limit:
            total = query.count()
            if total > limit:
                query = query.offset(total - limit)
        models = query.all()
        return [self._model_to_entity(m) for m in models]

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todos los mensajes de una sesión de chat.

        Args:
            session_id (str): Identificador de la sesión a limpiar.

        Returns:
            int: Número de mensajes eliminados.
        """
        count = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .count()
        )
        self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).delete()
        self.db.commit()
        return count

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión, en orden cronológico.

        Se usa para construir el contexto conversacional que se envía a la IA.
        Obtiene los más recientes (ordenados descendente) y los invierte
        para presentarlos en orden cronológico.

        Args:
            session_id (str): Identificador de la sesión.
            count (int): Número de mensajes recientes a obtener.

        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico (más antiguos primero).
        """
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )
        models.reverse()
        return [self._model_to_entity(m) for m in models]

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """
        Convierte un modelo ORM ChatMemoryModel a una entidad de dominio ChatMessage.

        Maneja la conversión de timestamps naive a timezone-aware UTC.

        Args:
            model (ChatMemoryModel): Modelo ORM a convertir.

        Returns:
            ChatMessage: Entidad de dominio con los datos del modelo.
        """
        ts = model.timestamp
        if ts and ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=ts or datetime.now(timezone.utc),
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """
        Convierte una entidad de dominio ChatMessage a un modelo ORM ChatMemoryModel.

        Args:
            entity (ChatMessage): Entidad de dominio a convertir.

        Returns:
            ChatMemoryModel: Modelo ORM listo para persistir en la base de datos.
        """
        ts = entity.timestamp
        if ts and ts.tzinfo is not None:
            ts = ts.replace(tzinfo=None)
        return ChatMemoryModel(
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=ts,
        )
