from datetime import date
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from segmentasi_ahc_api.app.models.customers import Customer
    from segmentasi_ahc_api.app.models.products import Product


class Transaction(SQLModel, table=True):
    __tablename__ = 'transactions'

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    transaction_date: date
    total_amount: float

    customer: "Customer" = Relationship(back_populates="transactions")
    transaction_items: List["TransactionItem"] = Relationship(back_populates="transaction")


class TransactionItem(SQLModel, table=True):
    __tablename__ = 'transaction_items'

    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: int = Field(foreign_key="transactions.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int
    unit_price: float
    total_price: float

    transaction: "Transaction" = Relationship(back_populates="transaction_items")
    product: "Product" = Relationship(back_populates="transaction_items")
