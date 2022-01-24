from uuid import UUID

from .main import celery
from .services import FavoriteProductService


@celery.task()
def create_favorite_product(customer_id: UUID, product_id: UUID) -> None:
    favorite_product_service = FavoriteProductService()
    favorite_product_service.create_favorite_product(customer_id, product_id)
