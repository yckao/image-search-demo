from functools import lru_cache
from typing import AsyncGenerator

from fastapi import Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import AsyncSessionLocal
from src.interfaces.clip import CLIPServiceProtocol
from src.interfaces.storage import StorageServiceProtocol
from src.clip.service import CLIPService
from src.storage.service_s3 import S3Service
from src.exceptions import UnsupportedStorageProviderError


@lru_cache()
def get_clip_service() -> CLIPServiceProtocol:
    return CLIPService(model_name=settings.model_name, model_path=settings.model_path)


@lru_cache()
def get_storage_service(
    provider_name: str = Path(),
) -> StorageServiceProtocol:
    if provider_name == "s3":
        return S3Service(
            endpoint_url=settings.s3_endpoint_url,
            bucket_name=settings.s3_bucket_name,
            access_key=settings.s3_access_key,
            secret_key=settings.s3_secret_key,
        )

    raise UnsupportedStorageProviderError(provider_name=provider_name)


def get_default_storage_provider() -> StorageServiceProtocol:
    return get_storage_service(settings.storage_provider)


async def get_database() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
