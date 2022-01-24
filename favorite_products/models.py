from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from .main import db


class Customer(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return '<Customer(name="{}", email="{}")>'.format(self.name, self.email)

    def __str__(self):
        return "{}, {}".format(self.name, self.email)


class FavoriteProduct(db.Model):
    __table_args__ = (db.UniqueConstraint("customer_id", "product_id"),)

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("customer.id"), nullable=False
    )
    customer = db.relationship(
        "Customer", backref=db.backref("favorite_products", lazy=True)
    )
    product_id = db.Column(UUID(as_uuid=True), default=uuid4, nullable=False)

    def __repr__(self):
        return '<FavoriteProduct(product_id="{}", customer_id={})>'.format(
            self.product_id, self.customer_id
        )

    def __str__(self):
        return str(self.product_id)
