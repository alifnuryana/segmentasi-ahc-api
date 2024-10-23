from sqlmodel import Session, select

from segmentasi_ahc_api.app.models.customers import Customer
from segmentasi_ahc_api.app.models.products import Product


def get_or_create_product(db: Session, product_name: str, category: str, size: str, unit_price: float):
    product = db.exec(
        select(Product).where(
            Product.name == product_name,
            Product.category == category,
            Product.size == size,
            Product.unit_price == unit_price
        )
    ).first()

    if not product:
        product = Product(name=product_name, category=category, size=size, unit_price=unit_price)
        db.add(product)
        db.commit()
        db.refresh(product)

    return product


def get_or_create_customer(db: Session, customer_name: str):
    customer = db.exec(
        select(Customer).where(Customer.name == customer_name)
    ).first()

    if not customer:
        customer = Customer(name=customer_name)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    return customer
