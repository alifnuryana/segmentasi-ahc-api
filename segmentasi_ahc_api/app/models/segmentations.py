from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from segmentasi_ahc_api.app.models.clusters import Cluster


class Segmentation(SQLModel, table=True):
    __tablename__ = 'segmentations'

    segmentation_id: Optional[int] = Field(default=None, primary_key=True)
    cluster_id: int = Field(foreign_key="clusters.id")
    segment_feature: str
    segment_value: str

    cluster: "Cluster" = Relationship(back_populates="segmentations")
