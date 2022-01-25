from favorite_products.models import Customer, FavoriteProduct

FAKE_PRODUCT_ID = "fca18708-e2c8-4cc5-befb-a66720842424"
FAKE_CUSTOMER_ID = "fca18708-e2c8-4cc5-befb-a66720842425"


def test_customer_repr():
    customer = Customer(name="test", email="test@test.com")
    assert repr(customer) == '<Customer(name="test", email="test@test.com")>'


def test_customer_str():
    customer = Customer(name="test", email="test@test.com")
    assert str(customer) == "test, test@test.com"


def test_favorite_product_repr():
    favorite_product = FavoriteProduct(
        product_id=FAKE_PRODUCT_ID, customer_id=FAKE_CUSTOMER_ID
    )
    assert repr(favorite_product) == f'<FavoriteProduct(product_id="{FAKE_PRODUCT_ID}", customer_id="{FAKE_CUSTOMER_ID}")>'


def test_favorite_product_str():
    favorite_product = FavoriteProduct(
        product_id=FAKE_PRODUCT_ID, customer_id=FAKE_CUSTOMER_ID
    )
    assert str(favorite_product) == "fca18708-e2c8-4cc5-befb-a66720842424"
