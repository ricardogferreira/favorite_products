from uuid import UUID

from sqlalchemy.exc import IntegrityError

from .exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
    ProductAlreadyExistsError,
)
from .main import db
from .models import Customer, FavoriteProduct


def create_customer(name: str, email: str) -> Customer:
    """Criar cliente"""
    customer = Customer(name=name, email=email)
    try:
        save_changes(customer)
    except IntegrityError:
        raise CustomerAlreadyExistsError
    return customer


def get_customer_by_email(email: str) -> Customer:
    """Buscar cliente por email"""
    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        raise CustomerNotFoundError
    return customer


def get_customer_by_id(id: str) -> Customer:
    """Buscar cliente por id"""
    customer = Customer.query.filter_by(id=id).first()
    if not customer:
        raise CustomerNotFoundError
    return customer


def get_customers() -> list:
    """Buscar todos clientes"""
    return Customer.query.all()


def get_favorite_products_by_customer(customer: Customer) -> list:
    "Buscar todos produtos favoritos de um cliente"
    return customer.favorite_products


def create_favorite_product(customer: Customer, product_id: UUID) -> list:
    """Criar um produto favorito"""
    favorite_product = FavoriteProduct(product_id=product_id)
    customer.favorite_products.append(favorite_product)
    try:
        save_changes(customer)
    except IntegrityError:
        raise ProductAlreadyExistsError
    return favorite_product


def delete_customer(customer: Customer) -> Customer:
    """Deletar cliente do banco de dados"""
    db.session.delete(customer)
    db.session.commit()


def update_customer(customer: Customer, name: str) -> Customer:
    """Atualizar cliente"""
    customer.name = name
    save_changes(customer)
    return customer


def save_changes(data) -> None:
    """Faz o commit das alterações"""
    db.session.add(data)
    db.session.commit()
