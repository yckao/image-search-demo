from uuid import UUID

from src.exceptions import ServiceException


class ImageNotFoundError(ServiceException):
    status_code = 404
    error_code = "IMAGE_NOT_FOUND"
    detail = "Image not found"

    def __init__(self, image_id: UUID):
        self.detail = f"Image with id {image_id} not found"
        super().__init__(
            status_code=self.status_code, error_code=self.error_code, detail=self.detail
        )


class NoImageAvailableError(ServiceException):
    status_code = 404
    error_code = "NO_IMAGE_AVAILABLE"
    detail = "No image available for model"

    def __init__(self, model_name: str):
        self.detail = f"No image available for model {model_name}"
        super().__init__(
            status_code=self.status_code, error_code=self.error_code, detail=self.detail
        )


class SearchQueryNotFoundError(ServiceException):
    status_code = 404
    error_code = "SEARCH_QUERY_NOT_FOUND"
    detail = "Search query not found"

    def __init__(self, query_id: UUID):
        self.detail = f"Search query with id {query_id} not found"
        super().__init__(
            status_code=self.status_code, error_code=self.error_code, detail=self.detail
        )


class SearchFeedbackAlreadyExistsError(ServiceException):
    status_code = 400
    error_code = "SEARCH_FEEDBACK_ALREADY_EXISTS"
    detail = "Search feedback already exists"

    def __init__(self, query_id: UUID):
        self.detail = f"Search feedback for query with id {query_id} already exists"
        super().__init__(
            status_code=self.status_code, error_code=self.error_code, detail=self.detail
        )
