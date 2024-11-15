from typing import TYPE_CHECKING, final

import attr

from src.repositories.users import UsersRepository
from src.services.user_create import UserCreate, UserCreateError

if TYPE_CHECKING:
    from src.entities.user import User


class UserRegisterError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)


@final
@attr.dataclass(slots=True, frozen=True)
class UserRegister:
    _username: str
    _password1: str
    _password2: str

    def __call__(self) -> "User":
        users_repo = UsersRepository()
        user_creator = UserCreate(users_repo)

        try:
            return user_creator(
                username=self._username,
                password1=self._password1,
                password2=self._password2,
            )
        except UserCreateError as exc:
            raise UserRegisterError(exc.msg) from exc
