from favorite_products.services import CustomerService, FavoriteProductService

FAKE_PRODUCT_ID = "fca18708-e2c8-4cc5-befb-a66720842424"
FAKE_CUSTOMER_ID = "fca18708-e2c8-4cc5-befb-a66720842425"


def test_delete_customer(mocker):
    customer_id = "fca18708-e2c8-4cc5-befb-a66720842424"
    mock_customer = mocker.Mock()
    mock_get_customer_by_id = mocker.patch(
        "favorite_products.services.get_customer_by_id", return_value=mock_customer
    )
    mock_delete_customer = mocker.patch("favorite_products.services.delete_customer")
    CustomerService.delete_customer(customer_id)
    mock_get_customer_by_id.assert_called_with(customer_id)
    mock_delete_customer.assert_called_with(mock_customer)


def test_update_customer(mocker):
    customer_id = "fca18708-e2c8-4cc5-befb-a66720842424"
    mock_customer = mocker.Mock()
    name = "test123333"
    mock_get_customer_by_id = mocker.patch(
        "favorite_products.services.get_customer_by_id", return_value=mock_customer
    )
    mock_update_customer = mocker.patch("favorite_products.services.update_customer")
    CustomerService.update_customer(customer_id, name)
    mock_get_customer_by_id.assert_called_with(customer_id)
    mock_update_customer.assert_called_with(mock_customer, name)


def test_get_customer_or_customers_return_customer(mocker):
    customer_id = "fca18708-e2c8-4cc5-befb-a66720842424"
    mock_customer = mocker.Mock()
    mock_get_customer_by_id = mocker.patch(
        "favorite_products.services.get_customer_by_id", return_value=mock_customer
    )
    customer = CustomerService.get_customer_or_customers(customer_id)
    mock_get_customer_by_id.assert_called_with(customer_id)
    assert customer == mock_customer


def test_get_customer_or_customers_return_customers(mocker):
    customer_id = None
    mock_customers = [mocker.Mock(), mocker.Mock()]
    mock_get_customers = mocker.patch(
        "favorite_products.services.get_customers", return_value=mock_customers
    )
    customers = CustomerService.get_customer_or_customers(customer_id)
    mock_get_customers.assert_called()
    assert customers == mock_customers


def test_create_customer(mocker):
    nome = "test"
    email = "test@test.com"
    mock_customer = mocker.Mock()
    mock_create_customer = mocker.patch(
        "favorite_products.services.create_customer", return_value=mock_customer
    )
    customer = CustomerService.create_customer(nome, email)
    mock_create_customer.assert_called_with(nome, email)
    assert customer == mock_customer


def test_create_favorite_product(mocker):
    mock_customer = mocker.Mock()
    mock_get_customer_by_id = mocker.patch(
        "favorite_products.services.get_customer_by_id", return_value=mock_customer
    )
    mock_favorite_product = mocker.Mock()
    mock_create_favorite_product = mocker.patch(
        "favorite_products.services.create_favorite_product",
        return_value=mock_favorite_product,
    )
    favorite_product_service = FavoriteProductService()
    mocker.patch.object(favorite_product_service, "challenge_luizalabs_client")
    favorite_product = favorite_product_service.create_favorite_product(
        FAKE_CUSTOMER_ID, FAKE_PRODUCT_ID
    )

    mock_get_customer_by_id.assert_called_with(FAKE_CUSTOMER_ID)
    mock_create_favorite_product.assert_called_with(mock_customer, FAKE_PRODUCT_ID)
    assert favorite_product == mock_favorite_product


def test_get_favorite_products_by_customer(mocker):
    mock_customer = mocker.Mock()
    mock_get_customer_by_id = mocker.patch(
        "favorite_products.services.get_customer_by_id", return_value=mock_customer
    )
    mock_favorite_products = [mocker.Mock(), mocker.Mock()]
    mock_get_favorite_products_by_customer = mocker.patch(
        "favorite_products.services.get_favorite_products_by_customer",
        return_value=mock_favorite_products,
    )
    favorite_product_service = FavoriteProductService()
    mock_challenge_luizalabs_client = mocker.patch.object(
        favorite_product_service, "challenge_luizalabs_client"
    )
    favorite_product_service.get_favorite_products_by_customer(FAKE_CUSTOMER_ID)

    mock_get_customer_by_id.assert_called_with(FAKE_CUSTOMER_ID)
    mock_get_favorite_products_by_customer.assert_called_with(mock_customer)
    assert mock_challenge_luizalabs_client.get_product_by_product_id.call_count == 2
