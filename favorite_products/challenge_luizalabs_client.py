import json
from uuid import UUID

import requests
from requests.exceptions import HTTPError
from requests.status_codes import codes

from .config import CHALLENGE_LUIZALABS_API_URL
from .exceptions import ProductApiNotFoundError


class ChallengeLuizalabsClient:
    def __init__(self, url=CHALLENGE_LUIZALABS_API_URL):
        self.url = url

    def request_to_json(self, url: str) -> json:
        """
        Faz a requisição ao servidor externo (github),
        valida a resposta e retorna o json que esta no corpo
        """
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_product_by_product_id(self, product_id: UUID) -> json:
        """
        Busca lista de repositórios no github por username
        """
        url = f"{self.url}/product/{product_id}/"
        try:
            product = self.request_to_json(url)
            return product
        except HTTPError as http_error:
            if http_error.response.status_code == codes.NOT_FOUND:
                raise ProductApiNotFoundError
            raise
