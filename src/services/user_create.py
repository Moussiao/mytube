from typing import TYPE_CHECKING, final

import attr

from src.core.password import get_password_hash

if TYPE_CHECKING:
    from src.entities.user import User
    from src.repositories.users import UsersRepositoryInterface


class UserCreateError(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)


class UserExistsError(UserCreateError):
    pass


@final
class PasswordsNotEqualError(UserCreateError):
    pass


@final
@attr.dataclass(slots=True, frozen=True)
class UserCreate:
    _users_repo: "UsersRepositoryInterface"

    def __call__(self, username: str, password1: str, password2: str) -> "User":
        if password1 != password2:
            raise PasswordsNotEqualError("Passwords must be equal")

        if self._users_repo.is_exists(username):
            raise UserExistsError(f"User with {username=} allready created")

        password_hash = get_password_hash(password1)
        return self._users_repo.create(username=username, password=password_hash)
