from io import BytesIO
from typing import Protocol, AsyncIterator, TypedDict


from pydantic import BaseModel


class StorageFile(BaseModel):
    provider: str
    key: str


class FileStreamData(TypedDict):
    chunk_iter: AsyncIterator[bytes]
    content_type: str
    content_length: int
    filename: str


class StorageServiceProtocol(Protocol):
    async def upload_file(
        self,
        filename: str,
        file: BytesIO,
        content_type: str = "application/octet-stream",
    ) -> StorageFile: ...

    async def get_file_stream(
        self, key: str, chunk_size: int = 69 * 1024
    ) -> FileStreamData: ...

    async def format_download_url(self, base_url: str, key: str) -> str: ...
