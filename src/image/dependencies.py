from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.dependencies import (
    get_clip_service,
    get_database,
    get_default_storage_provider,
)
from src.image.repositories import ImageRepository
from src.image.service import ImageService
from src.interfaces.clip import CLIPServiceProtocol
from src.interfaces.storage import StorageServiceProtocol


def get_image_repository(
    database: AsyncSession = Depends(get_database),
) -> ImageRepository:
    return ImageRepository(database)


def get_image_service(
    image_repository: ImageRepository = Depends(get_image_repository),
    clip_service: CLIPServiceProtocol = Depends(get_clip_service),
    storage_service: StorageServiceProtocol = Depends(get_default_storage_provider),
) -> ImageService:
    return ImageService(image_repository, storage_service, clip_service)
