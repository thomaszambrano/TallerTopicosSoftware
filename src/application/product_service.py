"""
Módulo del servicio de aplicación para productos.

Implementa los casos de uso relacionados con la gestión de productos
del e-commerce. Orquesta las operaciones entre el dominio y la
capa de infraestructura usando inyección de dependencias.
"""

from typing import List, Optional
from ..domain.entities import Product
from ..domain.repositories import IProductRepository
from ..domain.exceptions import ProductNotFoundError, InvalidProductDataError
from .dtos import ProductDTO


class ProductService:
    """
    Servicio de aplicación para la gestión de productos.

    Implementa los casos de uso del e-commerce relacionados con productos,
    como listar, buscar, crear, actualizar y eliminar zapatos del catálogo.

    Attributes:
        product_repo (IProductRepository): Repositorio de productos inyectado.
    """

    def __init__(self, product_repo: IProductRepository):
        """
        Inicializa el servicio con el repositorio de productos.

        Args:
            product_repo (IProductRepository): Implementación del repositorio
                a usar para acceder a los datos de productos.
        """
        self.product_repo = product_repo

    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos disponibles en el catálogo.

        Returns:
            List[ProductDTO]: Lista de todos los productos como DTOs.

        Example:
            >>> products = service.get_all_products()
            >>> len(products)
            10
        """
        products = self.product_repo.get_all()
        return [self._entity_to_dto(p) for p in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """
        Busca un producto específico por su identificador.

        Args:
            product_id (int): ID del producto a buscar.

        Returns:
            ProductDTO: Datos del producto encontrado.

        Raises:
            ProductNotFoundError: Si no existe un producto con ese ID.

        Example:
            >>> product = service.get_product_by_id(1)
            >>> product.name
            'Nike Air Zoom Pegasus'
        """
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return self._entity_to_dto(product)

    def search_products(
        self, brand: Optional[str] = None, category: Optional[str] = None
    ) -> List[ProductDTO]:
        """
        Filtra productos por marca y/o categoría.

        Si se proporcionan ambos filtros, se aplican en secuencia.
        Si no se proporciona ninguno, retorna todos los productos.

        Args:
            brand (Optional[str]): Marca por la que filtrar (ej. 'Nike').
            category (Optional[str]): Categoría por la que filtrar (ej. 'Running').

        Returns:
            List[ProductDTO]: Lista de productos que coinciden con los filtros.
        """
        if brand and category:
            products = self.product_repo.get_by_brand(brand)
            products = [p for p in products if p.category.lower() == category.lower()]
        elif brand:
            products = self.product_repo.get_by_brand(brand)
        elif category:
            products = self.product_repo.get_by_category(category)
        else:
            products = self.product_repo.get_all()
        return [self._entity_to_dto(p) for p in products]

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """
        Crea un nuevo producto en el catálogo.

        Convierte el DTO a entidad del dominio para aplicar validaciones
        de negocio antes de persistir el producto.

        Args:
            product_dto (ProductDTO): Datos del nuevo producto a crear.

        Returns:
            ProductDTO: El producto creado con su ID asignado.

        Raises:
            InvalidProductDataError: Si los datos del producto violan reglas de negocio.
        """
        try:
            entity = self._dto_to_entity(product_dto)
            saved = self.product_repo.save(entity)
            return self._entity_to_dto(saved)
        except ValueError as e:
            raise InvalidProductDataError(str(e))

    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """
        Actualiza los datos de un producto existente.

        Args:
            product_id (int): ID del producto a actualizar.
            product_dto (ProductDTO): Nuevos datos del producto.

        Returns:
            ProductDTO: El producto actualizado.

        Raises:
            ProductNotFoundError: Si el producto no existe.
            InvalidProductDataError: Si los nuevos datos son inválidos.
        """
        existing = self.product_repo.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(product_id)
        try:
            entity = self._dto_to_entity(product_dto)
            entity.id = product_id
            saved = self.product_repo.save(entity)
            return self._entity_to_dto(saved)
        except ValueError as e:
            raise InvalidProductDataError(str(e))

    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto del catálogo.

        Args:
            product_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó correctamente.

        Raises:
            ProductNotFoundError: Si el producto no existe.
        """
        existing = self.product_repo.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(product_id)
        return self.product_repo.delete(product_id)

    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene únicamente los productos con stock disponible.

        Returns:
            List[ProductDTO]: Lista de productos disponibles para la venta.
        """
        products = self.product_repo.get_all()
        available = [p for p in products if p.is_available()]
        return [self._entity_to_dto(p) for p in available]

    def _entity_to_dto(self, entity: Product) -> ProductDTO:
        """
        Convierte una entidad de dominio Product a su DTO correspondiente.

        Args:
            entity (Product): Entidad de producto a convertir.

        Returns:
            ProductDTO: DTO con los datos del producto.
        """
        return ProductDTO(
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

    def _dto_to_entity(self, dto: ProductDTO) -> Product:
        """
        Convierte un DTO ProductDTO a su entidad de dominio correspondiente.

        Args:
            dto (ProductDTO): DTO a convertir.

        Returns:
            Product: Entidad de dominio con los datos del DTO.
        """
        return Product(
            id=dto.id,
            name=dto.name,
            brand=dto.brand,
            category=dto.category,
            size=dto.size,
            color=dto.color,
            price=dto.price,
            stock=dto.stock,
            description=dto.description,
        )
