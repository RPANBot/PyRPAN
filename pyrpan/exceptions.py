class BaseException(Exception):
    ...


class InvalidRequest(BaseException):
    ...


class APIError(BaseException):
    ...


class RateLimitExceeded(BaseException):
    ...
