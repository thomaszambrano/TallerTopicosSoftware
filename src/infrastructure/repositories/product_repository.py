"""
Módulo del repositorio concreto de productos.

Implementa la interfaz IProductRepository usando SQLAlchemy y SQLite.
Convierte entre modelos ORM y entidades del dominio.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.entities import Product
from ...domain.repositories import IProductRepository
from ..db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """
    Implementación concreta del repositorio de productos usando SQLAlchemy.

    Implementa el patrón Repository para abstraer el acceso a la base de datos.
    Convierte entre modelos ORM (ProductModel) y entidades del dominio (Product).

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

    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos de la base de datos.

        Returns:
            List[Product]: Lista de entidades Product. Lista vacía si no hay productos.
        """
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Busca un producto por su ID en la base de datos.

        Args:
            product_id (int): ID del producto a buscar.

        Returns:
            Optional[Product]: Entidad Product si existe, None si no se encuentra.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene todos los productos de una marca específica.

        La búsqueda es case-insensitive usando LOWER().

        Args:
            brand (str): Nombre de la marca a buscar.

        Returns:
            List[Product]: Lista de productos de esa marca.
        """
        models = (
            self.db.query(ProductModel)
            .filter(ProductModel.brand.ilike(f"%{brand}%"))
            .all()
        )
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene todos los productos de una categoría específica.

        La búsqueda es case-insensitive.

        Args:
            category (str): Nombre de la categoría a buscar.

        Returns:
            List[Product]: Lista de productos de esa categoría.
        """
        models = (
            self.db.query(ProductModel)
            .filter(ProductModel.category.ilike(f"%{category}%"))
            .all()
        )
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en la base de datos.

        Si el producto tiene ID, lo actualiza. Si no tiene ID, crea uno nuevo
        y retorna la entidad con el ID generado.

        Args:
            product (Product): Entidad de producto a guardar.

        Returns:
            Product: El producto guardado con su ID asignado.
        """
        if product.id:
            model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
            if model:
                model.name = product.name
                model.brand = product.brand
                model.category = product.category
                model.size = product.size
                model.color = product.color
                model.price = product.price
                model.stock = product.stock
                model.description = product.description
            else:
                model = self._entity_to_model(product)
                self.db.add(model)
        else:
            model = self._entity_to_model(product)
            self.db.add(model)

        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto de la base de datos por su ID.

        Args:
            product_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un modelo ORM ProductModel a una entidad de dominio Product.

        Args:
            model (ProductModel): Modelo ORM a convertir.

        Returns:
            Product: Entidad de dominio con los datos del modelo.
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description or "",
        )

    def _entity_to_model(self, entity: Product) -> ProductModel:
        """
        Convierte una entidad de dominio Product a un modelo ORM ProductModel.

        Args:
            entity (Product): Entidad de dominio a convertir.

        Returns:
            ProductModel: Modelo ORM listo para persistir en la base de datos.
        """
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )
