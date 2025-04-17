from pydantic import BaseModel, field_validator
from typing import Optional, List


class ArtObject(BaseModel):
    objectID: int
    title: Optional[str] = None
    artistDisplayName: Optional[str] = None
    objectDate: Optional[str] = None
    primaryImage: Optional[str] = None


class SearchResults(BaseModel):
    total: int
    objectIDs: Optional[List[int]] = None

    @field_validator("objectIDs", mode="before")
    def ensure_object_ids_list(cls, value):
        return value if value is not None else []
