"""
Módulo de configuración de fixtures para los tests.

Provee fixtures reutilizables para crear entidades y mocks necesarios
en las pruebas unitarias de la aplicación.
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock
from src.domain.entities import Product, ChatMessage, ChatContext


@pytest.fixture
def valid_product():
    """
    Fixture que retorna un producto válido para usar en tests.

    Returns:
        Product: Entidad Product con todos los campos válidos.
    """
    return Product(
        id=1,
        name="Air Zoom Pegasus 40",
        brand="Nike",
        category="Running",
        size="42",
        color="Negro",
        price=120.0,
        stock=5,
        description="Zapato de running con tecnología Air Zoom.",
    )


@pytest.fixture
def valid_chat_message():
    """
    Fixture que retorna un mensaje de chat válido para usar en tests.

    Returns:
        ChatMessage: Entidad ChatMessage con datos válidos.
    """
    return ChatMessage(
        id=1,
        session_id="test_session",
        role="user",
        message="Busco zapatos para correr",
        timestamp=datetime.now(timezone.utc),
    )


@pytest.fixture
def mock_product_repo():
    """
    Fixture que retorna un mock del repositorio de productos.

    Returns:
        MagicMock: Mock del IProductRepository con métodos básicos configurados.
    """
    repo = MagicMock()
    return repo


@pytest.fixture
def mock_chat_repo():
    """
    Fixture que retorna un mock del repositorio de chat.

    Returns:
        MagicMock: Mock del IChatRepository con métodos básicos configurados.
    """
    repo = MagicMock()
    repo.get_recent_messages.return_value = []
    return repo


@pytest.fixture
def mock_ai_service():
    """
    Fixture que retorna un mock del servicio de IA Gemini.

    Returns:
        MagicMock: Mock del GeminiService configurado para retornar una respuesta de prueba.
    """
    service = MagicMock()
    import asyncio

    async def mock_generate(*args, **kwargs):
        return "Respuesta de prueba del asistente de IA."

    service.generate_response = mock_generate
    return service
