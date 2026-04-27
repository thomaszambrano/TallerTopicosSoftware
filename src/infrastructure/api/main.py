"""
Módulo principal de la aplicación FastAPI.

Define todos los endpoints de la API REST del e-commerce de zapatos
con chat inteligente. Configura CORS, inicialización de base de datos
y manejo de errores.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from ..db.database import get_db, init_db
from ..repositories.product_repository import SQLProductRepository
from ..repositories.chat_repository import SQLChatRepository
from ..llm_providers.gemini_service import GeminiService
from ...application.product_service import ProductService
from ...application.chat_service import ChatService
from ...application.dtos import (
    ProductDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ChatHistoryDTO,
)
from ...domain.exceptions import ProductNotFoundError, ChatServiceError

app = FastAPI(
    title="E-commerce Zapatos con Chat IA",
    description=(
        "API REST de e-commerce de zapatos con asistente de IA conversacional. "
        "Permite consultar productos y chatear con un asistente inteligente "
        "powered by Google Gemini AI para encontrar el zapato perfecto."
    ),
    version="1.0.0",
    contact={
        "name": "Thomas Osorio",
        "url": "https://github.com/thomasosorio",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """
    Evento de inicio de la aplicación.

    Se ejecuta al arrancar el servidor. Inicializa la base de datos,
    crea las tablas necesarias y carga los datos iniciales de productos
    si la base de datos está vacía.
    """
    init_db()


@app.get("/", tags=["General"])
def read_root():
    """
    Endpoint raíz con información básica de la API.

    Retorna metadatos de la API: nombre, versión, descripción
    y lista de endpoints disponibles.

    Returns:
        dict: Información básica de la API con endpoints disponibles.

    Example:
        GET /
        Response: {"api": "E-commerce Zapatos con Chat IA", "version": "1.0.0", ...}
    """
    return {
        "api": "E-commerce Zapatos con Chat IA",
        "version": "1.0.0",
        "descripcion": "API de e-commerce con asistente de IA powered by Google Gemini",
        "endpoints": {
            "productos": "/products",
            "producto_por_id": "/products/{id}",
            "chat": "/chat",
            "historial_chat": "/chat/history/{session_id}",
            "health": "/health",
            "documentacion": "/docs",
        },
    }


@app.get("/products", response_model=List[ProductDTO], tags=["Productos"])
def get_products(
    brand: str = Query(None, description="Filtrar por marca (ej: Nike, Adidas)"),
    category: str = Query(None, description="Filtrar por categoría (ej: Running, Casual)"),
    db: Session = Depends(get_db),
):
    """
    Obtiene la lista de productos disponibles en el catálogo.

    Permite filtrar opcionalmente por marca y/o categoría usando
    query parameters. Sin filtros, retorna todos los productos.

    Args:
        brand (str, optional): Nombre de la marca para filtrar.
        category (str, optional): Nombre de la categoría para filtrar.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[ProductDTO]: Lista de productos con toda su información.

    Example:
        GET /products
        GET /products?brand=Nike
        GET /products?category=Running
        GET /products?brand=Nike&category=Running
    """
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    return service.search_products(brand=brand, category=category)


@app.get("/products/{product_id}", response_model=ProductDTO, tags=["Productos"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles completos de un producto específico.

    Args:
        product_id (int): Identificador único del producto a buscar.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        ProductDTO: Datos completos del producto encontrado.

    Raises:
        HTTPException 404: Si no existe un producto con el ID especificado.

    Example:
        GET /products/1
        Response: {"id": 1, "name": "Air Zoom Pegasus 40", "brand": "Nike", ...}
    """
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    try:
        return service.get_product_by_id(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/chat", response_model=ChatMessageResponseDTO, tags=["Chat IA"])
async def chat(request: ChatMessageRequestDTO, db: Session = Depends(get_db)):
    """
    Procesa un mensaje del usuario y retorna una respuesta generada por IA.

    Flujo interno:
    1. Obtiene el catálogo de productos disponibles.
    2. Recupera el historial reciente de la sesión.
    3. Genera una respuesta contextual usando Google Gemini AI.
    4. Persiste el mensaje y la respuesta en el historial.
    5. Retorna la respuesta al cliente.

    Args:
        request (ChatMessageRequestDTO): Mensaje del usuario con session_id.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        ChatMessageResponseDTO: Respuesta de la IA con session_id, mensaje
            del usuario, respuesta del asistente y timestamp.

    Raises:
        HTTPException 500: Si ocurre un error al procesar el mensaje o
            comunicarse con el servicio de IA.

    Example:
        POST /chat
        Body: {"session_id": "usuario_001", "message": "Busco zapatos Nike"}
        Response: {
            "session_id": "usuario_001",
            "user_message": "Busco zapatos Nike",
            "assistant_message": "Tengo varios modelos Nike disponibles...",
            "timestamp": "2024-01-15T10:30:00"
        }
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    try:
        ai_service = GeminiService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    service = ChatService(product_repo, chat_repo, ai_service)
    try:
        return await service.process_message(request)
    except ChatServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al procesar el mensaje: {str(e)}",
        )


@app.get(
    "/chat/history/{session_id}",
    response_model=List[ChatHistoryDTO],
    tags=["Chat IA"],
)
def get_chat_history(
    session_id: str,
    limit: int = Query(10, description="Número máximo de mensajes a retornar"),
    db: Session = Depends(get_db),
):
    """
    Obtiene el historial de mensajes de una sesión de chat.

    Retorna los mensajes en orden cronológico (del más antiguo al más reciente).

    Args:
        session_id (str): Identificador único de la sesión de conversación.
        limit (int): Número máximo de mensajes a retornar. Por defecto 10.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[ChatHistoryDTO]: Lista de mensajes del historial con rol y timestamp.

    Example:
        GET /chat/history/usuario_001?limit=5
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service_placeholder = None

    class _MockAI:
        pass

    service = ChatService(product_repo, chat_repo, _MockAI())
    return service.get_session_history(session_id, limit=limit)


@app.delete("/chat/history/{session_id}", tags=["Chat IA"])
def delete_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Elimina el historial completo de mensajes de una sesión de chat.

    Útil para limpiar conversaciones antiguas o cuando el usuario quiere
    iniciar una nueva conversación desde cero.

    Args:
        session_id (str): Identificador de la sesión cuyo historial se eliminará.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        dict: Confirmación con la cantidad de mensajes eliminados.

    Example:
        DELETE /chat/history/usuario_001
        Response: {"message": "Historial eliminado", "mensajes_eliminados": 4}
    """

    class _MockAI:
        pass

    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    service = ChatService(product_repo, chat_repo, _MockAI())
    deleted = service.clear_session_history(session_id)
    return {"message": "Historial eliminado", "mensajes_eliminados": deleted}


@app.get("/health", tags=["General"])
def health_check():
    """
    Verifica el estado de salud de la API.

    Endpoint de health check para monitoreo y verificación de disponibilidad.
    Retorna el estado actual y el timestamp del servidor.

    Returns:
        dict: Estado del servicio con timestamp actual en UTC.

    Example:
        GET /health
        Response: {"status": "ok", "timestamp": "2024-01-15T10:30:00"}
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "E-commerce Zapatos con Chat IA",
    }
