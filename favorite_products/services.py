from uuid import UUID

from .challenge_luizalabs_client import ChallengeLuizalabsClient
from .respository import (
    create_customer,
    create_favorite_product,
    delete_customer,
    get_customer_by_id,
    get_customers,
    get_favorite_products_by_customer,
    update_customer,
)


class CustomerService:
    @staticmethod
    def delete_customer(id):
        customer = get_customer_by_id(id)
        delete_customer(customer)

    def update_customer(self, id, name):
        customer = get_customer_by_id(id)
        customer = update_customer(customer, name)
        return customer

    @staticmethod
    def get_customer_or_customers(id):
        if id:
            return get_customer_by_id(id)
        return get_customers()

    @staticmethod
    def create_customer(nome, email):
        return create_customer(nome, email)


class FavoriteProductService:
    def __init__(self):
        self.challenge_luizalabs_client = ChallengeLuizalabsClient()

    def create_favorite_product(self, customer_id: UUID, product_id: UUID) -> list:
        """Criar um produto favorito"""
        customer = get_customer_by_id(customer_id)
        self.challenge_luizalabs_client.get_product_by_product_id(product_id)
        favorite_product = create_favorite_product(customer, product_id)
        return favorite_product

    @staticmethod
    def get_favorite_products_by_customer(customer_id: UUID):
        customer = get_customer_by_id(customer_id)
        favorite_products = get_favorite_products_by_customer(customer)
        return favorite_products
