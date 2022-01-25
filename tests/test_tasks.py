from favorite_products.tasks import create_favorite_product

FAKE_PRODUCT_ID = "fca18708-e2c8-4cc5-befb-a66720842424"
FAKE_CUSTOMER_ID = "fca18708-e2c8-4cc5-befb-a66720842425"


def test_create_favorite_product(mocker):
    mock_favorite_product_service = mocker.Mock()
    MockFavoriteProductService = mocker.patch(
        "favorite_products.tasks.FavoriteProductService",
        return_value=mock_favorite_product_service,
    )
    create_favorite_product(FAKE_CUSTOMER_ID, FAKE_PRODUCT_ID)
    MockFavoriteProductService.assert_called()
    mock_favorite_product_service.create_favorite_product.assert_called_with(
        FAKE_CUSTOMER_ID, FAKE_PRODUCT_ID
    )
