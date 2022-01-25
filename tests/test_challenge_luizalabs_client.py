import pytest
from requests.exceptions import HTTPError
from requests.status_codes import codes

from favorite_products.challenge_luizalabs_client import \
    ChallengeLuizalabsClient
from favorite_products.exceptions import ProductApiNotFoundError

FAKE_PRODUCT_ID = "fca18708-e2c8-4cc5-befb-a66720842424"


def test_get_product_by_product_id(mocker):
    challenge_luizalabs_client = ChallengeLuizalabsClient(url='https://test.com/api')
    mock_product = mocker.Mock()
    mock_request_to_json = mocker.patch.object(challenge_luizalabs_client, 'request_to_json', return_value=mock_product)
    product = challenge_luizalabs_client.get_product_by_product_id(FAKE_PRODUCT_ID)
    mock_request_to_json.assert_called_with('https://test.com/api/product/fca18708-e2c8-4cc5-befb-a66720842424/')
    assert product == mock_product


def test_get_product_by_product_id_raises_product_api_not_found_error(mocker):
    challenge_luizalabs_client = ChallengeLuizalabsClient(url='https://test.com/api')
    mock_response = mocker.Mock()
    mock_response.status_code = codes.NOT_FOUND
    mocker.patch.object(challenge_luizalabs_client, 'request_to_json', side_effect=HTTPError(response=mock_response))
    with pytest.raises(ProductApiNotFoundError):
        challenge_luizalabs_client.get_product_by_product_id(FAKE_PRODUCT_ID)


def test_get_product_by_product_id_raises_http_error(mocker):
    challenge_luizalabs_client = ChallengeLuizalabsClient(url='https://test.com/api')
    mock_response = mocker.Mock()
    mocker.patch.object(challenge_luizalabs_client, 'request_to_json', side_effect=HTTPError(response=mock_response))
    with pytest.raises(HTTPError):
        challenge_luizalabs_client.get_product_by_product_id(FAKE_PRODUCT_ID)


def test_request_to_json(mocker):
    challenge_luizalabs_client = ChallengeLuizalabsClient(url='https://test.com/api')
    mock_requests = mocker.patch('favorite_products.challenge_luizalabs_client.requests')
    mock_get = mocker.Mock()
    mock_requests.get.return_value = mock_get
    challenge_luizalabs_client.request_to_json('https://test.com/api/abc')
    mock_requests.get.assert_called_with('https://test.com/api/abc')
    mock_get.raise_for_status.assert_called()
    mock_get.json.assert_called()
