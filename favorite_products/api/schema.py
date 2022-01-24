from flask_restx import fields

from favorite_products.main import api


schemaPostCustomer = api.model(
    "Post Customer",
    {"name": fields.String(required=True), "email": fields.String(required=True)},
)

schemaPutCustomer = api.model(
    "Customer",
    {"name": fields.String(required=True)},
)

schemaRetrieveCustomer = api.model(
    "Retrieve Customer",
    {
        "id": fields.String(),
        "name": fields.String(),
        "email": fields.String(),
    },
)

schemaRetrieveFavoriteProduct = api.model(
    "Retrieve Favorite Product",
    {
        "id": fields.String(),
        "product_id": fields.String(),
    },
)

schemaPostFavoriteProduct = api.model(
    "Post Favorite Product",
    {
        "product_id": fields.String(required=True),
    },
)
