from uuid import UUID

from flask_restx import abort, Resource

from favorite_products.exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
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

parser = namespace.parser()
parser.add_argument(
    "Authorization", type=str, location="headers", required=True, help="Token de acesso"
)


class BaseResource(Resource):
    method_decorators = [authenticate]


class CustomerResourceDetail(BaseResource):
    @namespace.marshal_with(schemaRetrieveCustomer)
    @namespace.doc(parser=parser)
    def get(self, id: UUID = None):
        """
        Detalhar dados do cliente
        """
        return CustomerService.get_customer_or_customers(id)

    @namespace.doc(parser=parser)
    def delete(self, id: UUID):
        """
        Deletar um cliente
        """
        try:
            CustomerService.delete_customer(id)
            return "", 204
        except CustomerNotFoundError:
            abort(404, message="Customer not found")

    @namespace.marshal_with(schemaRetrieveCustomer)
    @namespace.doc(parser=parser, body=schemaPutCustomer, validate=True)
    def put(self, id: UUID):
        """Atualizar dados de um cliente"""
        payload = self.api.payload
        customer_service = CustomerService()
        try:
            customer = customer_service.update_customer(id, payload["name"])
            return customer, 201
        except CustomerNotFoundError:
            abort(404, message="Customer not found")


class CustomerResource(BaseResource):
    @namespace.marshal_list_with(schemaRetrieveCustomer)
    @namespace.marshal_with(schemaRetrieveCustomer)
    @namespace.doc(parser=parser)
    def get(self):
        """
        Listar clientes
        """
        return CustomerService.get_customer_or_customers()

    @namespace.marshal_with(schemaRetrieveCustomer)
    @namespace.doc(parser=parser, body=schemaPostCustomer, validate=True)
    def post(self):
        """Inserir um novo cliente"""
        payload = self.api.payload
        try:
            customer = CustomerService.create_customer(**payload)
        except CustomerAlreadyExistsError:
            abort(409, message="Email already exists")
        return customer, 201


class FavoriteProductResource(BaseResource):
    @namespace.marshal_list_with(schemaRetrieveFavoriteProduct)
    @namespace.doc(parser=parser)
    def get(self, customer_id: UUID):
        """
        Lista produtos favoritos de um cliente
        """
        favorite_product_service = FavoriteProductService()
        favorite_products = favorite_product_service.get_favorite_products_by_customer(
            customer_id
        )
        return favorite_products

    @namespace.doc(parser=parser, body=schemaPostFavoriteProduct, validate=True)
    def post(self, customer_id: UUID):
        """Inserir um novo produto na lista de favoritos de um cliente"""
        payload = self.api.payload
        create_favorite_product.apply_async(args=(customer_id,), kwargs=payload)
        return {"message": "Enviado para processar com sucesso"}, 201


namespace.add_resource(CustomerResource, "/")
namespace.add_resource(CustomerResourceDetail, "/<string:id>/")

namespace.add_resource(
    FavoriteProductResource, "/<string:customer_id>/favorite_products"
)
