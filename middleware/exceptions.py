class APIException(Exception):
    """Base class for API exceptions."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class BadRequestException(APIException):
    """Exception for bad requests (400)."""
    def __init__(self, detail: str = "Bad request"):
        super().__init__(400, detail)


class UnauthorizedException(APIException):
    """Exception for unauthorized access (401)."""
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(401, detail)


class ForbiddenException(APIException):
    """Exception for forbidden access (403)."""
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(403, detail)


class NotFoundException(APIException):
    """Exception for not found resources (404)."""
    def __init__(self, detail: str = "Not found"):
        super().__init__(404, detail)


class InternalErrorException(APIException):
    """Exception for internal server error (500)."""
    def __init__(self, detail: str = "Internal error"):
        super().__init__(500, detail)
