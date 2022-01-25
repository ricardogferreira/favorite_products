pep8:
	isort app --check-only --skip migrations

fix-import:
	isort favorite_products
	isort tests

test:
	pytest -v

coverage:
	pytest -v --cov -vv

coverage-report: coverage
	coverage report -m

serve:
	FLASK_APP=favorite_products FLASK_ENV=development flask run