import asyncio
from uuid import UUID

from PIL import ImageFile

from src.image.models import Image, ImageEmbedding, SearchFeedback, SearchQuery
from src.image.repositories import ImageRepository
from src.image.schemas import (
    ImageSchema,
    CreateImageResponse,
    GetImageResponse,
    RatingSchema,
    SearchQuerySchema,
    SearchResponse,
    SearchFeedbackResponse,
)
from src.image.utils import pil_image_to_io
from src.interfaces.clip import CLIPServiceProtocol
from src.interfaces.storage import StorageServiceProtocol

from src.dependencies import get_storage_service


class ImageService:
    def __init__(
        self,
        image_repository: ImageRepository,
        storage_service: StorageServiceProtocol,
        clip_service: CLIPServiceProtocol,
    ):
        self.image_repository = image_repository
        self.storage_service = storage_service
        self.clip_service = clip_service

    async def create_image(self, base_url: str, file: ImageFile) -> CreateImageResponse:
        io_file = await pil_image_to_io(file)
        storage_file, embedding = await asyncio.gather(
            self.storage_service.upload_file(
                io_file.filename, io_file.file, io_file.content_type
            ),
            self.clip_service.image_embedding(file),
        )
        embedding = await self.clip_service.image_embedding(file)

        image = Image(
            storage_provider=storage_file.provider,
            storage_key=storage_file.key,
        )

        embedding = ImageEmbedding(
            model_name=self.clip_service.model_name,
            embedding=embedding,
        )

        image = await self.image_repository.create_image(image, embedding)

        return CreateImageResponse(
            id=image.id,
            storage_provider=image.storage_provider,
            storage_key=image.storage_key,
            created_at=image.created_at,
            url=await self.storage_service.format_download_url(
                base_url, image.storage_key
            ),
        )

    async def get_image(self, base_url: str, image_id: UUID):
        image = await self.image_repository.get_image(image_id)
        storage_service = get_storage_service(image.storage_provider)

        return GetImageResponse(
            id=image.id,
            storage_provider=image.storage_provider,
            storage_key=image.storage_key,
            created_at=image.created_at,
            url=await storage_service.format_download_url(base_url, image.storage_key),
        )

    async def search_images(self, base_url: str, query: str):
        embeddings = await self.clip_service.text_embedding(query)
        search_query = SearchQuery(
            model_name=self.clip_service.model_name,
            query_text=query,
            query_embedding=embeddings,
        )
        search_query = await self.image_repository.create_search_query(search_query)
        image = search_query.result_image

        storage_service = get_storage_service(image.storage_provider)

        return SearchResponse(
            id=search_query.id,
            model_name=search_query.model_name,
            query_text=search_query.query_text,
            image=ImageSchema(
                id=image.id,
                storage_provider=image.storage_provider,
                storage_key=image.storage_key,
                created_at=image.created_at,
                url=await storage_service.format_download_url(
                    base_url, image.storage_key
                ),
            ),
            created_at=search_query.created_at,
        )

    async def search_feedback(self, query_id: UUID, rating: RatingSchema):
        search_query = await self.image_repository.get_search_query(query_id)
        search_feedback = await self.image_repository.create_search_feedback(
            SearchFeedback(search_query_id=query_id, rating=rating)
        )

        return SearchFeedbackResponse(
            id=search_feedback.id,
            query=SearchQuerySchema(
                id=search_query.id,
                model_name=search_query.model_name,
                query_text=search_query.query_text,
                created_at=search_query.created_at,
            ),
            rating=search_feedback.rating,
            created_at=search_feedback.created_at,
        )
