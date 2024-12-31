from src.exceptions import ServiceException


class ObjectNotFoundError(ServiceException):
    status_code = 404
    error_code = "OBJECT_NOT_FOUND"
    detail = "Object not found in storage"

    def __init__(self, provider_name: str, key: str):

        self.detail = f"Object {key} not found in {provider_name} storage"
        super().__init__(
            status_code=self.status_code, error_code=self.error_code, detail=self.detail
        )
