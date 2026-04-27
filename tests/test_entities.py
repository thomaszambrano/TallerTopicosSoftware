"""
Tests unitarios para las entidades del dominio.

Verifica las validaciones de negocio y el comportamiento de las entidades
Product, ChatMessage y ChatContext.
"""

import pytest
from datetime import datetime, timezone
from src.domain.entities import Product, ChatMessage, ChatContext


class TestProduct:
    """Tests para la entidad Product."""

    def test_crear_producto_valido(self):
        """Verifica que se puede crear un producto con datos válidos."""
        p = Product(
            id=1,
            name="Nike Air",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato running",
        )
        assert p.name == "Nike Air"
        assert p.price == 120.0
        assert p.stock == 5

    def test_precio_negativo_lanza_error(self):
        """Verifica que se lanza ValueError con precio negativo."""
        with pytest.raises(ValueError, match="precio"):
            Product(
                id=None,
                name="Test",
                brand="Brand",
                category="Cat",
                size="42",
                color="Negro",
                price=-10.0,
                stock=5,
                description="Desc",
            )

    def test_precio_cero_lanza_error(self):
        """Verifica que se lanza ValueError con precio igual a 0."""
        with pytest.raises(ValueError, match="precio"):
            Product(
                id=None,
                name="Test",
                brand="Brand",
                category="Cat",
                size="42",
                color="Negro",
                price=0.0,
                stock=5,
                description="Desc",
            )

    def test_stock_negativo_lanza_error(self):
        """Verifica que se lanza ValueError con stock negativo."""
        with pytest.raises(ValueError, match="stock"):
            Product(
                id=None,
                name="Test",
                brand="Brand",
                category="Cat",
                size="42",
                color="Negro",
                price=100.0,
                stock=-1,
                description="Desc",
            )

    def test_nombre_vacio_lanza_error(self):
        """Verifica que se lanza ValueError con nombre vacío."""
        with pytest.raises(ValueError, match="nombre"):
            Product(
                id=None,
                name="",
                brand="Brand",
                category="Cat",
                size="42",
                color="Negro",
                price=100.0,
                stock=5,
                description="Desc",
            )

    def test_is_available_con_stock(self, valid_product):
        """Verifica que is_available retorna True cuando hay stock."""
        assert valid_product.is_available() is True

    def test_is_available_sin_stock(self, valid_product):
        """Verifica que is_available retorna False cuando stock es 0."""
        valid_product.stock = 0
        assert valid_product.is_available() is False

    def test_reduce_stock_valido(self, valid_product):
        """Verifica que reduce_stock reduce correctamente el stock."""
        stock_inicial = valid_product.stock
        valid_product.reduce_stock(2)
        assert valid_product.stock == stock_inicial - 2

    def test_reduce_stock_insuficiente_lanza_error(self, valid_product):
        """Verifica que se lanza ValueError al reducir más del stock disponible."""
        with pytest.raises(ValueError):
            valid_product.reduce_stock(valid_product.stock + 1)

    def test_reduce_stock_cantidad_invalida_lanza_error(self, valid_product):
        """Verifica que se lanza ValueError con cantidad negativa o cero."""
        with pytest.raises(ValueError):
            valid_product.reduce_stock(0)
        with pytest.raises(ValueError):
            valid_product.reduce_stock(-1)

    def test_increase_stock(self, valid_product):
        """Verifica que increase_stock aumenta correctamente el stock."""
        stock_inicial = valid_product.stock
        valid_product.increase_stock(10)
        assert valid_product.stock == stock_inicial + 10

    def test_increase_stock_cantidad_invalida_lanza_error(self, valid_product):
        """Verifica que se lanza ValueError con cantidad negativa o cero."""
        with pytest.raises(ValueError):
            valid_product.increase_stock(0)
        with pytest.raises(ValueError):
            valid_product.increase_stock(-5)


class TestChatMessage:
    """Tests para la entidad ChatMessage."""

    def test_crear_mensaje_usuario_valido(self):
        """Verifica que se puede crear un mensaje de usuario válido."""
        msg = ChatMessage(
            id=1,
            session_id="session_test",
            role="user",
            message="Hola, busco zapatos",
            timestamp=datetime.now(timezone.utc),
        )
        assert msg.role == "user"
        assert msg.is_from_user() is True
        assert msg.is_from_assistant() is False

    def test_crear_mensaje_asistente_valido(self):
        """Verifica que se puede crear un mensaje de asistente válido."""
        msg = ChatMessage(
            id=2,
            session_id="session_test",
            role="assistant",
            message="Tenemos varios modelos disponibles.",
            timestamp=datetime.now(timezone.utc),
        )
        assert msg.role == "assistant"
        assert msg.is_from_assistant() is True
        assert msg.is_from_user() is False

    def test_role_invalido_lanza_error(self):
        """Verifica que se lanza ValueError con role inválido."""
        with pytest.raises(ValueError, match="role"):
            ChatMessage(
                id=None,
                session_id="session",
                role="admin",
                message="Mensaje",
                timestamp=datetime.now(timezone.utc),
            )

    def test_mensaje_vacio_lanza_error(self):
        """Verifica que se lanza ValueError con mensaje vacío."""
        with pytest.raises(ValueError, match="mensaje"):
            ChatMessage(
                id=None,
                session_id="session",
                role="user",
                message="",
                timestamp=datetime.now(timezone.utc),
            )

    def test_session_id_vacio_lanza_error(self):
        """Verifica que se lanza ValueError con session_id vacío."""
        with pytest.raises(ValueError, match="session_id"):
            ChatMessage(
                id=None,
                session_id="",
                role="user",
                message="Mensaje",
                timestamp=datetime.now(timezone.utc),
            )


class TestChatContext:
    """Tests para el Value Object ChatContext."""

    def _make_message(self, role: str, text: str) -> ChatMessage:
        """Helper para crear mensajes de prueba."""
        return ChatMessage(
            id=None,
            session_id="test",
            role=role,
            message=text,
            timestamp=datetime.now(timezone.utc),
        )

    def test_get_recent_messages_retorna_ultimos_n(self):
        """Verifica que get_recent_messages retorna los últimos N mensajes."""
        messages = [self._make_message("user", f"Mensaje {i}") for i in range(10)]
        context = ChatContext(messages=messages, max_messages=6)
        recent = context.get_recent_messages()
        assert len(recent) == 6
        assert recent[-1].message == "Mensaje 9"

    def test_get_recent_messages_con_pocos_mensajes(self):
        """Verifica que retorna todos los mensajes si hay menos que max_messages."""
        messages = [self._make_message("user", f"Msg {i}") for i in range(3)]
        context = ChatContext(messages=messages)
        assert len(context.get_recent_messages()) == 3

    def test_format_for_prompt_formato_correcto(self):
        """Verifica que format_for_prompt genera el formato correcto."""
        messages = [
            self._make_message("user", "Busco zapatos Nike"),
            self._make_message("assistant", "Tenemos el Air Zoom Pegasus."),
        ]
        context = ChatContext(messages=messages)
        formatted = context.format_for_prompt()
        assert "Usuario: Busco zapatos Nike" in formatted
        assert "Asistente: Tenemos el Air Zoom Pegasus." in formatted

    def test_format_for_prompt_vacio_si_sin_mensajes(self):
        """Verifica que retorna string vacío cuando no hay mensajes."""
        context = ChatContext(messages=[])
        assert context.format_for_prompt() == ""
