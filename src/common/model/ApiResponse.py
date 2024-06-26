from dataclasses import dataclass

from src.common.exception.BusinessException import BusinessException
from src.common.model import ErrorCode


@dataclass
class Error:
    code: str
    message: str

    @classmethod
    def build(cls, error: ErrorCode, msg: str = None):
        return cls(error.value, msg if msg else error.name)

    @classmethod
    def erorr(cls, code: str, msg: str):
        return cls(code, msg)


@dataclass
class ApiResponse:
    data: object | None
    error: Error | None

    @classmethod
    def success(cls, data):
        return cls(data, None)

    @classmethod
    def fail(cls, error: ErrorCode, msg: str = None):
        return cls(None, Error.build(error, msg))

    @classmethod
    def error(cls, e: BusinessException):
        code = e.error.code
        msg = (
            e.error.message
            if e.detail is None
            else f"{e.error.message} Error:{e.detail}"
        )
        return cls(None, Error.erorr(code, msg))
