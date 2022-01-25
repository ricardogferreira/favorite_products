from favorite_products.exceptions import (CustomerAlreadyExistsError,
                                          CustomerNotFoundError)
from favorite_products.models import Customer, FavoriteProduct
from favorite_products.services import CustomerService, FavoriteProductService


def test_get_customers(mocker, client):
    mocker.patch.object(
        CustomerService,
        "get_customer_or_customers",
        return_value=[
            Customer(
                email="test@test.com",
                id="fca18708-e2c8-4cc5-befb-a66720842424",
                name="test",
            ),
            Customer(
                email="test1@test.com",
                id="fca18708-e2c8-4cc5-befb-a66720842425",
                name="test1",
            ),
        ],
    )

    response = client.get("/api/customers/")
    assert 200 == response.status_code
    assert response.get_json() == [
        {
            "email": "test@test.com",
            "id": "fca18708-e2c8-4cc5-befb-a66720842424",
            "name": "test",
        },
        {
            "email": "test1@test.com",
            "id": "fca18708-e2c8-4cc5-befb-a66720842425",
            "name": "test1",
        },
    ]


def test_get_customer(mocker, client):
    mocker.patch.object(
        CustomerService,
        "get_customer_or_customers",
        return_value=Customer(
            email="test@test.com",
            id="fca18708-e2c8-4cc5-befb-a66720842424",
            name="test",
        ),
    )

    response = client.get("/api/customers/fca18708-e2c8-4cc5-befb-a66720842424/")
    assert 200 == response.status_code
    assert response.get_json() == {
        "email": "test@test.com",
        "id": "fca18708-e2c8-4cc5-befb-a66720842424",
        "name": "test",
    }


def test_delete_customer(mocker, client):
    mocker.patch.object(CustomerService, "delete_customer")

    response = client.delete("/api/customers/fca18708-e2c8-4cc5-befb-a66720842424/")
    assert 204 == response.status_code
    assert response.data == b""


def test_delete_customer_with_status_code_404(mocker, client):
    mocker.patch.object(
        CustomerService, "delete_customer", side_effect=CustomerNotFoundError
    )

    response = client.delete("/api/customers/fca18708-e2c8-4cc5-befb-a66720842424/")
    assert response.status_code == 404
    assert response.get_json() == {"message": "Customer not found"}


def test_update_customer(mocker, client):
    mocker.patch.object(
        CustomerService,
        "update_customer",
        return_value=Customer(
            email="test3@test.com",
            id="fca18708-e2c8-4cc5-befb-a66720842424",
            name="test",
        ),
    )

    response = client.put(
        "/api/customers/fca18708-e2c8-4cc5-befb-a66720842424/", json={"name": "test3"}
    )
    CustomerService.update_customer.assert_called_with(
        "fca18708-e2c8-4cc5-befb-a66720842424", "test3"
    )
    assert response.status_code == 201
    assert response.get_json() == {
        "email": "test3@test.com",
        "id": "fca18708-e2c8-4cc5-befb-a66720842424",
        "name": "test",
    }


def test_update_customer_with_status_code_404(mocker, client):
    mocker.patch.object(
        CustomerService, "update_customer", side_effect=CustomerNotFoundError
    )

    response = client.put(
        "/api/customers/fca18708-e2c8-4cc5-befb-a66720842424/", json={"name": "test3"}
    )
    CustomerService.update_customer.assert_called_with(
        "fca18708-e2c8-4cc5-befb-a66720842424", "test3"
    )
    assert response.status_code == 404
    assert response.get_json() == {"message": "Customer not found"}


def test_post_customer(mocker, client):
    mocker.patch.object(
        CustomerService,
        "create_customer",
        return_value=Customer(
            email="test3@test.com",
            id="fca18708-e2c8-4cc5-befb-a66720842424",
            name="test",
        ),
    )

    response = client.post(
        "/api/customers/", json={"name": "test3", "email": "test3@test.com"}
    )
    CustomerService.create_customer.assert_called_with(
        name="test3", email="test3@test.com"
    )
    assert response.status_code == 201
    assert response.get_json() == {
        "email": "test3@test.com",
        "id": "fca18708-e2c8-4cc5-befb-a66720842424",
        "name": "test",
    }


def test_post_customer_with_status_code_409(mocker, client):
    mocker.patch.object(
        CustomerService, "create_customer", side_effect=CustomerAlreadyExistsError
    )

    response = client.post(
        "/api/customers/", json={"name": "test3", "email": "test3@test.com"}
    )
    CustomerService.create_customer.assert_called_with(
        name="test3", email="test3@test.com"
    )
    assert response.status_code == 409
    assert response.get_json() == {"message": "Email already exists"}


def test_get_favorite_products(mocker, client):
    mocker.patch.object(
        FavoriteProductService,
        "get_favorite_products_by_customer",
        return_value=[
            FavoriteProduct(
                customer_id="fca18708-e2c8-4cc5-befb-a66720842424",
                product_id="fca18708-e2c8-4cc5-befb-a66720842424",
            ),
            FavoriteProduct(
                customer_id="fca18708-e2c8-4cc5-befb-a66720842424",
                product_id="fca18708-e2c8-4cc5-befb-a66720842425",
            ),
        ],
    )

    response = client.get(
        "/api/customers/fca18708-e2c8-4cc5-befb-a66720842424/favorite_products"
    )
    FavoriteProductService.get_favorite_products_by_customer.assert_called_with(
        "fca18708-e2c8-4cc5-befb-a66720842424"
    )
    assert 200 == response.status_code
    assert response.get_json() == [
        {"id": None, "image": None, "price": None, "title": None},
        {"id": None, "image": None, "price": None, "title": None},
    ]


def test_post_favorite_product(mocker, client):
    mock_create_favorite_product = mocker.patch(
        "favorite_products.api.resources.create_favorite_product"
    )

    response = client.post(
        "/api/customers/fca18708-e2c8-4cc5-befb-a66720842424/favorite_products",
        json={"product_id": "fca18708-e2c8-4cc5-befb-a66720842425"},
    )
    mock_create_favorite_product.apply_async.assert_called_with(
        args=("fca18708-e2c8-4cc5-befb-a66720842424",),
        kwargs={"product_id": "fca18708-e2c8-4cc5-befb-a66720842425"},
    )
    assert response.status_code == 201
    assert response.get_json() == {"message": "Enviado para processar com sucesso"}
