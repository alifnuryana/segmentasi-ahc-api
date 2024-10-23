from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from segmentasi_ahc_api.app.models.transactions import TransactionItem


class Product(SQLModel, table=True):
    __tablename__ = 'products'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    size: Optional[str] = None
    unit_price: float

    transaction_items: List["TransactionItem"] = Relationship(back_populates="product")
