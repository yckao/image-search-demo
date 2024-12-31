import enum
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class RatingSchema(enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class ImageSchema(BaseModel):
    id: UUID
    storage_provider: str
    storage_key: str
    created_at: datetime
    url: str


class SearchQuerySchema(BaseModel):
    id: UUID
    model_name: str
    query_text: str
    created_at: datetime


class CreateImageResponse(ImageSchema):
    pass


class GetImageResponse(ImageSchema):
    pass


class SearchResponse(SearchQuerySchema):
    image: ImageSchema


class SearchFeedbackResponse(BaseModel):
    id: UUID
    query: SearchQuerySchema
    rating: RatingSchema
    created_at: datetime


class IOFile(BaseModel):
    filename: str
    file: Any
    content_type: str
