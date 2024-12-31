from uuid import UUID

from fastapi import APIRouter, Depends, Request
from PIL import ImageFile

from src.image.dependencies import get_image_service
from src.image.schemas import (
    CreateImageResponse,
    SearchFeedbackResponse,
    SearchResponse,
    RatingSchema,
    GetImageResponse,
)
from src.image.service import ImageService
from src.image.utils import pil_image

router = APIRouter()


@router.post("", response_model=CreateImageResponse, status_code=201)
async def create_image(
    request: Request,
    file: ImageFile = Depends(pil_image),
    image_service: ImageService = Depends(get_image_service),
):
    return await image_service.create_image(str(request.base_url), file)


@router.get(
    "",
    responses={
        404: {
            "description": "No image available for model",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "NO_IMAGE_AVAILABLE",
                        "detail": "No image available for model",
                    }
                }
            },
        }
    },
    response_model=SearchResponse,
)
async def search_images(
    request: Request,
    query: str,
    image_service: ImageService = Depends(get_image_service),
):
    return await image_service.search_images(str(request.base_url), query)


@router.get(
    "/{image_id}",
    responses={
        404: {
            "description": "Image not found",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "IMAGE_NOT_FOUND",
                        "detail": "Image not found",
                    }
                }
            },
        }
    },
    response_model=GetImageResponse,
)
async def get_image(
    request: Request,
    image_id: UUID,
    image_service: ImageService = Depends(get_image_service),
):
    return await image_service.get_image(str(request.base_url), image_id)


@router.post(
    "/{query_id}/feedback",
    responses={
        400: {
            "description": "Search feedback already exists",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "SEARCH_FEEDBACK_ALREADY_EXISTS",
                        "detail": "Search feedback already exists",
                    }
                }
            },
        },
        404: {
            "description": "Search query not found",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "SEARCH_QUERY_NOT_FOUND",
                        "detail": "Search query not found",
                    }
                }
            },
        },
    },
    response_model=SearchFeedbackResponse,
)
async def search_feedback(
    query_id: UUID,
    rating: RatingSchema,
    image_service: ImageService = Depends(get_image_service),
):
    return await image_service.search_feedback(query_id, rating)
