from src.exceptions import ServiceException


class ClipGenerationError(ServiceException):

    status_code = 500
    error_code = "CLIP_GENERATION_ERROR"
    detail = "Clip generation failed"

    def __init__(self, detail: str):

        self.detail = detail
        super().__init__(
            status_code=self.status_code, error_code=self.error_code, detail=self.detail
        )
