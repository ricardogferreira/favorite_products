from pytest import fixture

from favorite_products.main import app


@fixture
def client():
    client = app.test_client()
    client.testing = True
    return client
