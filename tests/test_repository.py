from unittest import mock

import pytest
from sqlalchemy.exc import IntegrityError

from favorite_products.repository import (
    create_customer,
    create_favorite_product,
    get_customer_by_email,
    get_customer_by_id,
    get_customers,
    delete_customer,
    get_favorite_products_by_customer,
    update_customer,
    save_changes,
)

from favorite_products.exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
    ProductAlreadyExistsError,
)
from tests.test_services import FAKE_PRODUCT_ID

FAKE_CUSTOMER_ID = "fca18708-e2c8-4cc5-befb-a66720842425"


def test_create_customer(mocker):
    mock_save_changes = mocker.patch("favorite_products.repository.save_changes")
    customer = create_customer(name="test", email="test@test.com")
    mock_save_changes.assert_called_with(customer)


def test_create_customer_raises_customer_already_exists_error(mocker):
    mocker.patch(
        "favorite_products.repository.save_changes",
        side_effect=IntegrityError(mocker.Mock(), mocker.Mock(), mocker.Mock()),
    )

    with pytest.raises(CustomerAlreadyExistsError):
        create_customer(name="test", email="test@test.com")


def test_get_customer_by_email(mocker):
    MockCustomer = mocker.patch("favorite_products.repository.Customer")

    customer = get_customer_by_email("test@test.com")

    MockCustomer.query.filter_by.assert_called_with(email="test@test.com")
    MockCustomer.query.filter_by().first.assert_called()
    assert customer == MockCustomer.query.filter_by().first()


def test_get_customer_by_email_raises_customer_not_found_error(mocker):
    MockCustomer = mocker.patch("favorite_products.repository.Customer")
    MockCustomer.query.filter_by().first.return_value = None

    with pytest.raises(CustomerNotFoundError):
        get_customer_by_email("test@test.com")


def test_get_customer_by_id(mocker):
    MockCustomer = mocker.patch("favorite_products.repository.Customer")

    customer = get_customer_by_id(FAKE_PRODUCT_ID)

    MockCustomer.query.filter_by.assert_called_with(id=FAKE_PRODUCT_ID)
    MockCustomer.query.filter_by().first.assert_called()
    assert customer == MockCustomer.query.filter_by().first()


def test_get_customer_by_id_raises_customer_not_found_error(mocker):
    MockCustomer = mocker.patch("favorite_products.repository.Customer")
    MockCustomer.query.filter_by().first.return_value = None

    with pytest.raises(CustomerNotFoundError):
        get_customer_by_id(FAKE_PRODUCT_ID)


def test_get_customers(mocker):
    MockCustomer = mocker.patch("favorite_products.repository.Customer")

    customers = get_customers()

    MockCustomer.query.all.assert_called()
    customers == MockCustomer.query.all()


def test_get_favorite_products_by_customer(mocker):
    mock_customer = mocker.Mock()
    favorite_products = get_favorite_products_by_customer(mock_customer)
    mock_customer.favorite_products == favorite_products


def test_create_favorite_product(mocker):
    product_id = "fca18708-e2c8-4cc5-befb-a66720842424"
    mock_customer = mocker.Mock()
    mock_save_changes = mocker.patch("favorite_products.repository.save_changes")
    MockFavoriteProduct = mocker.patch("favorite_products.repository.FavoriteProduct")

    favorite_product = create_favorite_product(mock_customer, product_id=product_id)

    MockFavoriteProduct.assert_called_with(product_id=product_id)
    mock_customer.favorite_products.append.assert_called()
    mock_save_changes.assert_called_with(mock_customer)
    assert favorite_product == MockFavoriteProduct()


def test_create_favorite_product_raises_product_already_exists_error(mocker):
    product_id = "fca18708-e2c8-4cc5-befb-a66720842424"
    mock_customer = mocker.Mock()
    mocker.patch(
        "favorite_products.repository.save_changes",
        side_effect=IntegrityError(mocker.Mock(), mocker.Mock(), mocker.Mock()),
    )
    mocker.patch("favorite_products.repository.FavoriteProduct")

    with pytest.raises(ProductAlreadyExistsError):
        create_favorite_product(mock_customer, product_id=product_id)


def test_delete_customer(mocker):
    mock_customer = mocker.Mock()
    mock_db = mocker.patch("favorite_products.repository.db")

    delete_customer(mock_customer)

    mock_db.session.delete.assert_called_with(mock_customer)
    mock_db.session.commit.assert_called()


def test_update_customer(mocker):
    mock_customer = mocker.Mock()
    name = "test134"
    mock_save_changes = mocker.patch("favorite_products.repository.save_changes")

    customer = update_customer(mock_customer, name=name)

    mock_save_changes.assert_called_with(mock_customer)
    assert customer == mock_customer


def test_save_changes(mocker):
    mock_db = mocker.patch("favorite_products.repository.db")
    mock_customer = mocker.Mock()
    save_changes(mock_customer)

    mock_db.session.add.assert_called_with(mock_customer)
    mock_db.session.commit.assert_called()
