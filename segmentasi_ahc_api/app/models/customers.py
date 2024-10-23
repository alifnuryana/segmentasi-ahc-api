from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from segmentasi_ahc_api.app.models.clusters import Cluster
    from segmentasi_ahc_api.app.models.transactions import Transaction


class Customer(SQLModel, table=True):
    __tablename__ = 'customers'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    transactions: List["Transaction"] = Relationship(back_populates="customer")
    clusters: List["Cluster"] = Relationship(back_populates="customer")
