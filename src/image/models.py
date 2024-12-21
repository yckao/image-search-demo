import enum

from typing import List

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from src.database import Base
from src.utils.uuid import uuid7

class Image(Base):
    __tablename__ = "images"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    storage_provider: Mapped[str] = mapped_column(String(30), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    embedding: Mapped["ImageEmbedding"] = relationship("ImageEmbedding", back_populates="image")

class ImageEmbedding(Base):
    __tablename__ = "image_embeddings"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    image_id: Mapped[UUID] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    embedding: Mapped[List[float]] = mapped_column(Vector(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    image: Mapped["Image"] = relationship("Image", back_populates="embedding")
    __table_args__ = (
        Index("embedding_cosine_idx", embedding, postgresql_using="hnsw", postgresql_ops={"embedding": "vector_cosine_ops"}),
    )

class SearchQuery(Base):
    __tablename__ = "search_queries"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    model_name: Mapped[str] = mapped_column(String(30), nullable=False)
    query_text: Mapped[str] = mapped_column(String(255), nullable=False)
    query_embedding: Mapped[List[float]] = mapped_column(Vector(512), nullable=False)
    result_image_id: Mapped[UUID] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    feedback: Mapped["SearchFeedback"] = relationship("SearchFeedback", back_populates="search_query")
    result_image: Mapped["Image"] = relationship("Image")

class Rating(enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"

class SearchFeedback(Base):
    __tablename__ = "search_feedbacks"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7)
    search_query_id: Mapped[UUID] = mapped_column(ForeignKey("search_queries.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[bool] = mapped_column(Enum(Rating, native_enum=False, length=20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    search_query: Mapped["SearchQuery"] = relationship("SearchQuery", back_populates="feedback")