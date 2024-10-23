from datetime import date
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from segmentasi_ahc_api.app.models.customers import Customer
    from segmentasi_ahc_api.app.models.segmentations import Segmentation


class Cluster(SQLModel, table=True):
    __tablename__ = 'clusters'

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    cluster_label: int
    cluster_date: date

    customer: "Customer" = Relationship(back_populates="clusters")
    segmentations: List["Segmentation"] = Relationship(back_populates="cluster")
