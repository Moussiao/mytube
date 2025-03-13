from abc import ABC, abstractmethod
from typing import final

from src.core.repositories import MemoryRepository, NotFoundError, RepositoryError
from src.entities.user import User


class UsersRepositoryInterface(ABC):
    @abstractmethod
    def create(self, username: str, password: str) -> User: ...

    @abstractmethod
    def get_by_username(self, username: str) -> User: ...

    @abstractmethod
    def is_exists(self, username: str) -> bool: ...


class UserNotFoundError(NotFoundError):
    pass


class ManyUsersError(RepositoryError):
    pass


@final
class UsersRepository(MemoryRepository[int, User], UsersRepositoryInterface):
    def create(self, username: str, password: str) -> User:
        user_id = max(self._storage.keys()) + 1 if self._storage else 1
        user = User(id=user_id, username=username, password=password)
        self.push(key=user_id, value=user)
        return user

    def get_by_username(self, username: str) -> User:
        users = tuple(filter(lambda user: user.username == username, self._storage.values()))
        if not users:
            raise UserNotFoundError(f"User with {username=} does not exists")

        if len(users) > 1:
            raise ManyUsersError(f"User with {username=} more than one")

        return users[0]

    def is_exists(self, username: str) -> bool:
        return any(
            username.strip().lower() == user.username.strip().lower()
            for user in self._storage.values()
        )
