"""
Tests unitarios para los servicios de la capa de aplicación.

Verifica la lógica de negocio implementada en ProductService y ChatService
usando mocks para aislar las dependencias externas.
"""

import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import ProductDTO, ChatMessageRequestDTO
from src.domain.entities import Product, ChatMessage
from src.domain.exceptions import ProductNotFoundError, ChatServiceError


class TestProductService:
    """Tests para ProductService."""

    def _make_product(self, product_id=1, name="Nike Air", stock=5, price=100.0):
        """Helper para crear productos de prueba."""
        return Product(
            id=product_id,
            name=name,
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=price,
            stock=stock,
            description="Descripción de prueba",
        )

    def test_get_all_products_retorna_lista(self, mock_product_repo):
        """Verifica que get_all_products retorna la lista de productos como DTOs."""
        mock_product_repo.get_all.return_value = [self._make_product()]
        service = ProductService(mock_product_repo)
        result = service.get_all_products()
        assert len(result) == 1
        assert isinstance(result[0], ProductDTO)
        assert result[0].name == "Nike Air"

    def test_get_product_by_id_existente(self, mock_product_repo):
        """Verifica que get_product_by_id retorna el producto correcto."""
        mock_product_repo.get_by_id.return_value = self._make_product(product_id=1)
        service = ProductService(mock_product_repo)
        result = service.get_product_by_id(1)
        assert result.id == 1
        assert result.name == "Nike Air"

    def test_get_product_by_id_no_existente_lanza_error(self, mock_product_repo):
        """Verifica que se lanza ProductNotFoundError cuando el producto no existe."""
        mock_product_repo.get_by_id.return_value = None
        service = ProductService(mock_product_repo)
        with pytest.raises(ProductNotFoundError):
            service.get_product_by_id(999)

    def test_get_available_products_filtra_sin_stock(self, mock_product_repo):
        """Verifica que get_available_products solo retorna productos con stock."""
        productos = [
            self._make_product(product_id=1, stock=5),
            self._make_product(product_id=2, stock=0),
            self._make_product(product_id=3, stock=3),
        ]
        mock_product_repo.get_all.return_value = productos
        service = ProductService(mock_product_repo)
        result = service.get_available_products()
        assert len(result) == 2
        for p in result:
            assert p.stock > 0

    def test_delete_product_existente(self, mock_product_repo):
        """Verifica que delete_product elimina el producto correctamente."""
        mock_product_repo.get_by_id.return_value = self._make_product()
        mock_product_repo.delete.return_value = True
        service = ProductService(mock_product_repo)
        result = service.delete_product(1)
        assert result is True
        mock_product_repo.delete.assert_called_once_with(1)

    def test_delete_product_no_existente_lanza_error(self, mock_product_repo):
        """Verifica que se lanza ProductNotFoundError al eliminar producto inexistente."""
        mock_product_repo.get_by_id.return_value = None
        service = ProductService(mock_product_repo)
        with pytest.raises(ProductNotFoundError):
            service.delete_product(999)

    def test_search_products_por_marca(self, mock_product_repo):
        """Verifica que search_products filtra correctamente por marca."""
        mock_product_repo.get_by_brand.return_value = [self._make_product()]
        service = ProductService(mock_product_repo)
        result = service.search_products(brand="Nike")
        assert len(result) == 1
        mock_product_repo.get_by_brand.assert_called_once_with("Nike")

    def test_search_products_sin_filtros(self, mock_product_repo):
        """Verifica que search_products sin filtros retorna todos los productos."""
        mock_product_repo.get_all.return_value = [
            self._make_product(1), self._make_product(2)
        ]
        service = ProductService(mock_product_repo)
        result = service.search_products()
        assert len(result) == 2


class TestChatService:
    """Tests para ChatService."""

    def test_get_session_history(self, mock_product_repo, mock_chat_repo, mock_ai_service):
        """Verifica que get_session_history retorna el historial correctamente."""
        mock_chat_repo.get_session_history.return_value = [
            ChatMessage(
                id=1,
                session_id="test",
                role="user",
                message="Hola",
                timestamp=datetime.now(timezone.utc),
            )
        ]
        service = ChatService(mock_product_repo, mock_chat_repo, mock_ai_service)
        result = service.get_session_history("test", limit=10)
        assert len(result) == 1
        assert result[0].role == "user"

    def test_clear_session_history(self, mock_product_repo, mock_chat_repo, mock_ai_service):
        """Verifica que clear_session_history elimina el historial correctamente."""
        mock_chat_repo.delete_session_history.return_value = 4
        service = ChatService(mock_product_repo, mock_chat_repo, mock_ai_service)
        count = service.clear_session_history("test_session")
        assert count == 4
        mock_chat_repo.delete_session_history.assert_called_once_with("test_session")

    def test_process_message_exitoso(self, mock_product_repo, mock_chat_repo, mock_ai_service):
        """Verifica que process_message procesa y retorna la respuesta correctamente."""
        mock_product_repo.get_all.return_value = []
        mock_chat_repo.get_recent_messages.return_value = []
        mock_chat_repo.save_message.return_value = MagicMock()

        service = ChatService(mock_product_repo, mock_chat_repo, mock_ai_service)
        request = ChatMessageRequestDTO(session_id="session_001", message="Busco zapatos Nike")
        result = asyncio.run(service.process_message(request))

        assert result.session_id == "session_001"
        assert result.user_message == "Busco zapatos Nike"
        assert result.assistant_message == "Respuesta de prueba del asistente de IA."
        assert mock_chat_repo.save_message.call_count == 2

    def test_process_message_guarda_ambos_mensajes(
        self, mock_product_repo, mock_chat_repo, mock_ai_service
    ):
        """Verifica que process_message guarda el mensaje del usuario y la respuesta."""
        mock_product_repo.get_all.return_value = []
        mock_chat_repo.get_recent_messages.return_value = []
        mock_chat_repo.save_message.return_value = MagicMock()

        service = ChatService(mock_product_repo, mock_chat_repo, mock_ai_service)
        request = ChatMessageRequestDTO(session_id="s1", message="Hola")
        asyncio.run(service.process_message(request))

        assert mock_chat_repo.save_message.call_count == 2
        calls = mock_chat_repo.save_message.call_args_list
        saved_roles = [call[0][0].role for call in calls]
        assert "user" in saved_roles
        assert "assistant" in saved_roles
