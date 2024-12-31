from fastapi import APIRouter, Depends
from fastapi.responses import Response, StreamingResponse

from src.dependencies import get_storage_service
from src.interfaces.storage import StorageServiceProtocol

router = APIRouter()


class OctetStreamResponse(Response):
    media_type = "application/octet-stream"


@router.get(
    "/files/{key:path}",
    responses={
        404: {
            "description": "Object not found",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "OBJECT_NOT_FOUND",
                        "detail": "Object not found in storage",
                    }
                }
            },
        },
    },
    response_class=OctetStreamResponse,
)
async def get_file(
    key: str,
    storage_service: StorageServiceProtocol = Depends(get_storage_service),
):
    file_data = await storage_service.get_file_stream(key)

    return StreamingResponse(
        file_data.get("chunk_iter")(),
        media_type=file_data.get("content_type"),
        headers={
            "Content-Length": str(file_data.get("content_length")),
            "Content-Disposition": f"attachment; filename={file_data.get('filename')}",
        },
    )
