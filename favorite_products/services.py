from uuid import UUID

from favorite_products.models import Customer

from .challenge_luizalabs_client import ChallengeLuizalabsClient
from .repository import (create_customer, create_favorite_product,
                         delete_customer, get_customer_by_id, get_customers,
                         get_favorite_products_by_customer, update_customer)


class CustomerService:
    @staticmethod
    def delete_customer(id: UUID) -> None:
        customer = get_customer_by_id(id)
        delete_customer(customer)

    @staticmethod
    def update_customer(id: UUID, name: str) -> Customer:
        customer = get_customer_by_id(id)
        customer = update_customer(customer, name)
        return customer

    @staticmethod
    def get_customer_or_customers(id: UUID = None) -> Customer:
        if id:
            return get_customer_by_id(id)
        return get_customers()

    @staticmethod
    def create_customer(name: str, email: str) -> Customer:
        return create_customer(name, email)


class FavoriteProductService:
    def __init__(self):
        self.challenge_luizalabs_client = ChallengeLuizalabsClient()

    def create_favorite_product(self, customer_id: UUID, product_id: UUID) -> list:
        """Criar um produto favorito"""
        customer = get_customer_by_id(customer_id)
        self.challenge_luizalabs_client.get_product_by_product_id(product_id)
        favorite_product = create_favorite_product(customer, product_id)
        return favorite_product

    def get_favorite_products_by_customer(self, customer_id: UUID) -> list:
        customer = get_customer_by_id(customer_id)
        favorite_products = get_favorite_products_by_customer(customer)
        favorite_products_ = []
        """
        FIXME:
        Aqui o correto seria a api de produto ter um endpoint para buscar varios ids de uma vez.
        Não inseri os dados do produto no banco de dados porque tem um risco grande de serem alterados, principalmente o preço.
        """
        for favorite_product in favorite_products:
            favorite_products_.append(
                self.challenge_luizalabs_client.get_product_by_product_id(
                    favorite_product.product_id
                )
            )

        return favorite_products_
