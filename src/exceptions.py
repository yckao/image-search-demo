class ServiceException(Exception):
    status_code: int = 500
    error_code: str = "INTERNAL_SERVER_ERROR"
    detail: str = "An internal server error occurred."

    def __init__(
        self, status_code: int = None, error_code: str = None, detail: str = None
    ):

        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code
        self.detail = detail or self.detail

        super().__init__(self.status_code, self.error_code, self.detail)


class UnsupportedStorageProviderError(ServiceException):
    status_code = 400
    error_code = "UNSUPPORTED_STORAGE_PROVIDER"
    detail = "Unsupported storage provider"

    def __init__(self, provider_name: str):

        self.detail = f"Unsupported storage provider: {provider_name}"
        super().__init__(
            status_code=self.status_code, error_code=self.error_code, detail=self.detail
        )
