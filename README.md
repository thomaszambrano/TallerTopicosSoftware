# E-commerce Zapatos con Chat IA

API REST de e-commerce de zapatos con asistente conversacional inteligente usando **Clean Architecture** y **Google Gemini AI**.

## Descripción

Sistema de e-commerce que permite a los usuarios consultar un catálogo de zapatos y conversar con un asistente de IA que conoce el inventario completo, recuerda el historial de conversación y hace recomendaciones personalizadas.

## Tecnologías

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.11 | Lenguaje principal |
| FastAPI | 0.104.1 | Framework web y API REST |
| SQLAlchemy | 2.0.23 | ORM para base de datos |
| SQLite | — | Base de datos ligera |
| Google Gemini AI | 0.3.1 | Asistente conversacional inteligente |
| Pydantic | 2.5.0 | Validación de datos |
| Docker | — | Containerización |
| Pytest | 7.4.3 | Testing unitario |

## Arquitectura

El proyecto sigue **Clean Architecture** con 3 capas bien definidas:

```
┌─────────────────────────────────────────────────┐
│         INFRASTRUCTURE LAYER                    │
│  FastAPI + SQLAlchemy + Google Gemini           │
└─────────────────────────┬───────────────────────┘
                          │
┌─────────────────────────▼───────────────────────┐
│         APPLICATION LAYER                       │
│  Services + DTOs (casos de uso)                 │
└─────────────────────────┬───────────────────────┘
                          │
┌─────────────────────────▼───────────────────────┐
│         DOMAIN LAYER                            │
│  Entities + Repository Interfaces + Exceptions  │
└─────────────────────────────────────────────────┘
```

## Estructura del Proyecto

```
e-commerce-chat-ai/
├── src/
│   ├── config.py                    # Configuración global
│   ├── domain/                      # Capa de dominio
│   │   ├── entities.py              # Product, ChatMessage, ChatContext
│   │   ├── repositories.py          # IProductRepository, IChatRepository
│   │   └── exceptions.py            # Excepciones del dominio
│   ├── application/                 # Capa de aplicación
│   │   ├── dtos.py                  # DTOs con Pydantic
│   │   ├── product_service.py       # Casos de uso de productos
│   │   └── chat_service.py          # Casos de uso del chat
│   └── infrastructure/              # Capa de infraestructura
│       ├── api/main.py              # FastAPI endpoints
│       ├── db/                      # SQLAlchemy + modelos ORM
│       ├── repositories/            # Implementaciones de repositorios
│       └── llm_providers/           # Servicio Google Gemini
├── tests/                           # Tests unitarios
├── evidencias/                      # Screenshots del proyecto
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Requisitos Previos

- Python 3.10 o superior
- Docker y Docker Compose
- API Key de Google Gemini (gratis en [Google AI Studio](https://aistudio.google.com/app/apikey))

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd e-commerce-chat-ai
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` y agrega tu API key de Gemini:

```
GEMINI_API_KEY=AIzaSy...tu_key_aqui
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development
```

### 3. Ejecutar con Docker (Recomendado)

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost:8000`

### 4. Ejecutar sin Docker (desarrollo local)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Mac/Linux)
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear carpeta de datos
mkdir -p data

# Iniciar el servidor
uvicorn src.infrastructure.api.main:app --reload
```

## Uso

Una vez iniciada la aplicación:

- **API**: `http://localhost:8000`
- **Documentación Swagger**: `http://localhost:8000/docs`
- **Documentación ReDoc**: `http://localhost:8000/redoc`

## Endpoints

### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/products` | Lista todos los productos |
| GET | `/products?brand=Nike` | Filtra por marca |
| GET | `/products?category=Running` | Filtra por categoría |
| GET | `/products/{id}` | Obtiene producto por ID |

### Chat con IA

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/chat` | Envía mensaje al asistente de IA |
| GET | `/chat/history/{session_id}` | Obtiene historial de conversación |
| DELETE | `/chat/history/{session_id}` | Elimina historial de conversación |

### General

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Estado del servicio |

## Ejemplos de Uso

### Listar productos

```bash
curl http://localhost:8000/products
```

### Chatear con el asistente

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "usuario_001", "message": "Busco zapatos Nike para correr"}'
```

Respuesta:
```json
{
  "session_id": "usuario_001",
  "user_message": "Busco zapatos Nike para correr",
  "assistant_message": "¡Hola! Tengo dos excelentes opciones Nike para running...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### Consultar historial

```bash
curl http://localhost:8000/chat/history/usuario_001
```

## Tests

```bash
# Ejecutar todos los tests
pytest

# Con reporte de cobertura
pytest --cov=src tests/

# Mostrar detalles
pytest -v
```

## Docker

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## Autor

Thomas Osorio — Universidad EAFIT
