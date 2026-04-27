"""
Módulo de configuración global de la aplicación.

Carga las variables de entorno desde el archivo .env y las expone
como atributos de la clase Settings para uso en toda la aplicación.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Clase de configuración global de la aplicación.

    Lee las variables de entorno y las expone como atributos tipados.
    Proporciona valores por defecto seguros para desarrollo local.

    Attributes:
        GEMINI_API_KEY (str): Clave de API de Google Gemini para el servicio de IA.
        DATABASE_URL (str): URL de conexión a la base de datos SQLite.
        ENVIRONMENT (str): Entorno de ejecución ('development', 'production').
    """

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./data/ecommerce_chat.db"
    )
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()
