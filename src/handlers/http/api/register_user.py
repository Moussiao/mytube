import json
from dataclasses import dataclass
from enum import StrEnum
from http import HTTPStatus

from src.usecases.user_register import UserRegister, UserRegisterError


class ResponseStatus(StrEnum):
    ERROR = "error"
    SUCCESS = "success"


@dataclass(frozen=True, slots=True)
class ErrorResponse:
    detail: str
    status: ResponseStatus


@dataclass(frozen=True, slots=True)
class SuccessResponse:
    user: "UserResponse"
    status: ResponseStatus


@dataclass()
class UserResponse:
    id: int
    username: str


def register_user(request: dict[str, bytes]) -> tuple[HTTPStatus, ErrorResponse | SuccessResponse]:
    body = json.loads(request["body"].decode("utf-8"))
    user_register = UserRegister(
        username=str(body["username"]),
        password1=str(body["password1"]),
        password2=str(body["password2"]),
    )

    try:
        user = user_register()
    except UserRegisterError as exc:
        return HTTPStatus.UNPROCESSABLE_CONTENT, ErrorResponse(
            detail=exc.msg, status=ResponseStatus.ERROR
        )

    user_response = UserResponse(id=user.id, username=user.username)
    return HTTPStatus.OK, SuccessResponse(user=user_response, status=ResponseStatus.SUCCESS)
