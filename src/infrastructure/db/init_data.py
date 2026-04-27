"""
Módulo de datos iniciales de la base de datos.

Contiene la función para cargar productos de ejemplo al iniciar la aplicación
por primera vez. Los datos representan un catálogo realista de zapatos deportivos.
"""

from .models import ProductModel


def load_initial_data(db) -> None:
    """
    Carga datos iniciales de productos en la base de datos si está vacía.

    Verifica si ya existen productos antes de insertar para evitar duplicados.
    Si la base de datos está vacía, inserta 10 zapatos de diferentes marcas,
    categorías y tallas para demostrar la funcionalidad del e-commerce.

    Args:
        db: Sesión activa de SQLAlchemy.

    Returns:
        None

    Note:
        Esta función es segura de llamar múltiples veces: solo inserta datos
        si la tabla de productos está vacía.
    """
    count = db.query(ProductModel).count()
    if count > 0:
        return

    productos_iniciales = [
        ProductModel(
            name="Air Zoom Pegasus 40",
            brand="Nike",
            category="Running",
            size="42",
            color="Negro",
            price=120.0,
            stock=5,
            description="Zapato de running con tecnología Air Zoom para máxima amortiguación. "
                        "Ideal para corredores de larga distancia.",
        ),
        ProductModel(
            name="Ultraboost 23",
            brand="Adidas",
            category="Running",
            size="41",
            color="Blanco",
            price=180.0,
            stock=3,
            description="El Ultraboost 23 ofrece una increíble energía de retorno con su suela "
                        "de Boost. Perfecto para running y uso diario.",
        ),
        ProductModel(
            name="Suede Classic XXI",
            brand="Puma",
            category="Casual",
            size="40",
            color="Azul marino",
            price=75.0,
            stock=10,
            description="Un ícono del streetwear con suela de goma duradera. "
                        "Diseño clásico que nunca pasa de moda.",
        ),
        ProductModel(
            name="Chuck Taylor All Star",
            brand="Converse",
            category="Casual",
            size="43",
            color="Rojo",
            price=65.0,
            stock=8,
            description="El zapato más icónico del mundo. Canvas de alta calidad "
                        "con plantilla acolchada para mayor comodidad.",
        ),
        ProductModel(
            name="574 Core",
            brand="New Balance",
            category="Casual",
            size="44",
            color="Gris",
            price=95.0,
            stock=6,
            description="Clásico de New Balance con suela ENCAP para soporte "
                        "y amortiguación de todo el día.",
        ),
        ProductModel(
            name="Gel-Nimbus 25",
            brand="Asics",
            category="Running",
            size="42",
            color="Verde",
            price=160.0,
            stock=4,
            description="Máxima amortiguación para runners de alto rendimiento. "
                        "Tecnología Gel en el talón y antepié.",
        ),
        ProductModel(
            name="React Infinity Run 3",
            brand="Nike",
            category="Running",
            size="41",
            color="Azul",
            price=140.0,
            stock=7,
            description="Diseñado para reducir lesiones con su suela React foam. "
                        "Sistema Flywire para soporte dinámico.",
        ),
        ProductModel(
            name="Stan Smith",
            brand="Adidas",
            category="Casual",
            size="40",
            color="Blanco",
            price=85.0,
            stock=12,
            description="El clásico tenis de cuero de Adidas. Minimalista, "
                        "versátil y con más de 50 años de historia.",
        ),
        ProductModel(
            name="Speedcat OG",
            brand="Puma",
            category="Casual",
            size="39",
            color="Rojo",
            price=90.0,
            stock=5,
            description="Inspirado en los zapatos de conducción de los años 70. "
                        "Suela plana y diseño retro.",
        ),
        ProductModel(
            name="Oxford Elegance",
            brand="Clarks",
            category="Formal",
            size="43",
            color="Marrón",
            price=130.0,
            stock=9,
            description="Zapato formal de cuero genuino con suela de goma antideslizante. "
                        "Perfecto para ocasiones formales y de negocios.",
        ),
    ]

    db.add_all(productos_iniciales)
    db.commit()
