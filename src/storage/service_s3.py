from io import BytesIO

from aioboto3 import Session
from botocore import exceptions as boto_exceptions
import nanoid

from src.interfaces.storage import StorageFile, StorageServiceProtocol, FileStreamData
from src.storage.exceptions import ObjectNotFoundError


class S3Service(StorageServiceProtocol):
    provider_name: str = "s3"

    def __init__(
        self, endpoint_url: str, bucket_name: str, access_key: str, secret_key: str
    ):
        self.bucket_name = bucket_name
        self.session = Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.endpoint_url = endpoint_url

    async def upload_file(
        self,
        filename: str,
        file: BytesIO,
        content_type: str = "application/octet-stream",
    ) -> StorageFile:
        key = f"images/{nanoid.generate(size=10)}/{filename}"
        async with self.session.client("s3", endpoint_url=self.endpoint_url) as client:
            await client.upload_fileobj(
                file,
                self.bucket_name,
                key,
                ExtraArgs={
                    "ContentType": content_type or "application/octet-stream",
                },
            )

        return StorageFile(
            provider=self.provider_name,
            key=key,
        )

    async def get_file_stream(
        self, key: str, chunk_size: int = 69 * 1024
    ) -> FileStreamData:
        try:
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as get_metadata_client:
                head_metadata = await get_metadata_client.head_object(
                    Bucket=self.bucket_name, Key=key
                )
                content_length = head_metadata["ContentLength"]
                content_type = head_metadata["ContentType"]
                filename = key.split("/")[-1]
        except boto_exceptions.ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code in ["404", "NoSuchKey"]:
                raise ObjectNotFoundError(self.provider_name, key) from e
            raise

        async def generator():
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=key)
                try:
                    async for chunk in response["Body"].iter_chunks(chunk_size):
                        yield chunk
                finally:
                    response["Body"].close()

        return FileStreamData(
            chunk_iter=generator,
            content_type=content_type,
            content_length=content_length,
            filename=filename,
        )

    async def format_download_url(self, base_url: str, key: str) -> str:
        return f"{base_url.rstrip('/')}/storage/{self.provider_name}/files/{key}"
