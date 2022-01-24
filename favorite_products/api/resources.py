from uuid import UUID

from flask_restx import abort, Resource

from favorite_products.exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
    ProductAlreadyExistsError,
    ProductApiNotFoundError,
)
from favorite_products.main import api
from favorite_products.services import CustomerService, FavoriteProductService
from favorite_products.tasks import create_favorite_product

from .authenticate import authenticate
from .schema import (
    schemaPostCustomer,
    schemaPostFavoriteProduct,
    schemaPutCustomer,
    schemaRetrieveCustomer,
    schemaRetrieveFavoriteProduct,
)

namespace = api.namespace("customers")


class BaseResource(Resource):
    # method_decorators = [authenticate]
    ...


class CustomerResource(BaseResource):
    @namespace.marshal_list_with(schemaRetrieveCustomer)
    @namespace.marshal_with(schemaRetrieveCustomer)
    def get(self, id: UUID = None):
        """Mostra detalhes de um repositório do usuário,
        pode ser salvo no banco de dados local através do
        query param passado na url
        """
        return CustomerService.get_customer_or_customers()

    def delete(self, id: UUID):
        try:
            CustomerService.delete_customer(id)
            return "", 204
        except CustomerNotFoundError:
            abort(404, message="Customer not found")

    @namespace.marshal_with(schemaRetrieveCustomer)
    @namespace.doc(body=schemaPostCustomer, validate=True)
    def post(self):
        payload = self.api.payload
        try:
            customer = CustomerService.create_customer(**payload)
        except CustomerAlreadyExistsError:
            abort(409, message="Email already exists")
        return customer, 201

    @namespace.marshal_with(schemaRetrieveCustomer)
    @namespace.doc(body=schemaPutCustomer, validate=True)
    def put(self, id: UUID):
        payload = self.api.payload
        customer_service = CustomerService()
        try:
            customer = customer_service.update_customer(id, payload["name"])
            return customer, 201
        except CustomerNotFoundError:
            abort(404, message="Customer not found")


class FavoriteProductResource(BaseResource):
    @namespace.marshal_list_with(schemaRetrieveFavoriteProduct)
    def get(self, customer_id: UUID):
        """Lista repositorios de um usuário, pode ser retornado via cache(db) ou
        diretamente no github
        """
        favorite_products = FavoriteProductService.get_favorite_products_by_customer(
            customer_id
        )
        return favorite_products

    @namespace.marshal_with(schemaRetrieveFavoriteProduct)
    @namespace.doc(body=schemaPostFavoriteProduct, validate=True)
    def post(self, customer_id: UUID):
        payload = self.api.payload
        create_favorite_product.apply_async(args=(customer_id,), kwargs=payload)
        return {"message": "Enviado para processar com sucesso"}, 201


namespace.add_resource(CustomerResource, "/", "/<string:id>")
namespace.add_resource(
    FavoriteProductResource, "/<string:customer_id>/favorite_products"
)
