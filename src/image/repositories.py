from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.image.exceptions import (
    ImageNotFoundError,
    NoImageAvailableError,
    SearchFeedbackAlreadyExistsError,
    SearchQueryNotFoundError,
)
from src.image.models import Image, ImageEmbedding, SearchFeedback, SearchQuery


class ImageRepository:
    def __init__(self, database: AsyncSession):
        self.database = database

    async def create_image(self, image: Image, embedding: ImageEmbedding) -> Image:
        image.embedding = embedding
        embedding.image = image

        self.database.add(image)

        await self.database.commit()
        await self.database.refresh(image)

        return image

    async def get_image(self, image_id: UUID) -> Image:
        image = await self.database.get(
            Image,
            image_id,
        )

        if not image:
            raise ImageNotFoundError(image_id)

        return image

    async def create_search_query(self, query: SearchQuery) -> SearchQuery:
        image_embedding = await self.database.scalar(
            select(ImageEmbedding)
            .where(ImageEmbedding.model_name == query.model_name)
            .order_by(
                ImageEmbedding.embedding.cosine_distance(query.query_embedding),
                desc(ImageEmbedding.created_at),
            )
            .limit(1)
        )

        if not image_embedding:
            raise NoImageAvailableError(query.model_name)

        query.result_image_id = image_embedding.image_id
        self.database.add(query)
        await self.database.commit()
        await self.database.refresh(query, attribute_names=["result_image"])

        return query

    async def get_search_query(self, query_id: UUID) -> SearchQuery:
        query = await self.database.scalar(
            select(SearchQuery)
            .options(joinedload(SearchQuery.result_image))
            .where(SearchQuery.id == query_id)
        )

        if query is None:
            raise SearchQueryNotFoundError(query_id)

        return query

    async def create_search_feedback(
        self,
        search_feedback: SearchFeedback,
    ) -> SearchFeedback:
        try:
            self.database.add(search_feedback)
            await self.database.commit()
            await self.database.refresh(search_feedback)
        except IntegrityError as e:
            raise SearchFeedbackAlreadyExistsError(
                search_feedback.search_query_id
            ) from e

        return search_feedback
