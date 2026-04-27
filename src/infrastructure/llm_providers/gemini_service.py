"""
Módulo del servicio de integración con Google Gemini AI.

Implementa la comunicación con la API de Google Gemini para generar
respuestas contextuales en el chat del e-commerce de zapatos.
"""

import google.generativeai as genai
from ...config import settings
from ...domain.entities import ChatContext


class GeminiService:
    """
    Servicio de IA que integra Google Gemini para el chat del e-commerce.

    Formatea los prompts con el contexto del catálogo de productos y el
    historial de conversación para generar respuestas coherentes y útiles
    para los clientes de la tienda de zapatos.

    Attributes:
        model: Instancia del modelo generativo de Gemini configurado.
    """

    def __init__(self):
        """
        Inicializa el servicio configurando el cliente de Google Gemini.

        Lee la API key desde la configuración y crea el modelo generativo.
        Usa gemini-2.0-flash-exp para respuestas rápidas y de alta calidad.

        Raises:
            ValueError: Si GEMINI_API_KEY no está configurada en las variables de entorno.
        """
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY no está configurada. "
                "Agrega tu API key en el archivo .env"
            )
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

    async def generate_response(
        self, user_message: str, products: list, context: ChatContext
    ) -> str:
        """
        Genera una respuesta contextual usando Google Gemini AI.

        Construye un prompt completo que incluye el catálogo de productos,
        el historial de conversación y el mensaje actual del usuario para
        que la IA pueda dar recomendaciones precisas y coherentes.

        Args:
            user_message (str): Mensaje actual enviado por el usuario.
            products (list): Lista de entidades Product disponibles en el inventario.
            context (ChatContext): Contexto conversacional con el historial reciente.

        Returns:
            str: Respuesta generada por Gemini AI. Si ocurre un error,
                retorna un mensaje de fallback amigable.

        Example:
            >>> response = await service.generate_response(
            ...     "Busco zapatos Nike para correr",
            ...     products,
            ...     context
            ... )
            >>> "Nike" in response
            True
        """
        try:
            products_info = self.format_products_info(products)
            conversation_history = context.format_for_prompt()

            prompt = self._build_prompt(user_message, products_info, conversation_history)
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return (
                f"Lo siento, ocurrió un error al procesar tu mensaje. "
                f"Por favor, intenta de nuevo. (Error: {str(e)})"
            )

    def format_products_info(self, products: list) -> str:
        """
        Convierte la lista de productos a un texto legible para el prompt de IA.

        Formatea cada producto con su información más relevante para que
        la IA pueda hacer recomendaciones precisas.

        Args:
            products (list): Lista de entidades Product del catálogo.

        Returns:
            str: Texto formateado con la información de todos los productos.
                Cada línea tiene el formato: "- Nombre | Marca | Categoría | Talla | Color | $Precio | Stock: N unidades"

        Example:
            >>> info = service.format_products_info(products)
            >>> "Nike" in info
            True
        """
        if not products:
            return "No hay productos disponibles en este momento."

        lines = []
        for p in products:
            availability = f"{p.stock} unidades" if p.stock > 0 else "Agotado"
            lines.append(
                f"- {p.name} | {p.brand} | {p.category} | "
                f"Talla {p.size} | {p.color} | ${p.price:.2f} | Stock: {availability}"
            )
        return "\n".join(lines)

    def _build_prompt(
        self, user_message: str, products_info: str, conversation_history: str
    ) -> str:
        """
        Construye el prompt completo para enviar a Gemini AI.

        Integra el contexto del sistema, el catálogo de productos, el
        historial de conversación y el mensaje actual del usuario.

        Args:
            user_message (str): Mensaje actual del usuario.
            products_info (str): Catálogo de productos formateado.
            conversation_history (str): Historial reciente de la conversación.

        Returns:
            str: Prompt completo listo para enviar al modelo de IA.
        """
        history_section = ""
        if conversation_history:
            history_section = f"""
HISTORIAL DE CONVERSACIÓN RECIENTE:
{conversation_history}

"""

        return f"""Eres un asistente virtual experto en ventas de zapatos para un e-commerce llamado "Shoe Store".
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos según sus necesidades.

PRODUCTOS DISPONIBLES EN INVENTARIO:
{products_info}

INSTRUCCIONES:
- Sé amigable, profesional y entusiasta con los zapatos
- Usa el contexto del historial de conversación para dar respuestas coherentes
- Recomienda productos específicos del catálogo cuando sea apropiado
- Menciona siempre precios, tallas y disponibilidad de los productos que recomiendes
- Si un producto está agotado, infórmalo claramente y sugiere alternativas
- Si el cliente pregunta por algo que no está en el inventario, sé honesto y ofrece lo más parecido
- Responde siempre en español
- Mantén respuestas concisas pero informativas (máximo 3-4 párrafos)
- No inventes productos que no estén en el catálogo

{history_section}Usuario: {user_message}

Asistente:"""
