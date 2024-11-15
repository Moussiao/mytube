from collections.abc import Hashable
from typing import Any, Self

from src.core.singleton import Singleton


class RepositoryError(Exception):
    pass


class DuplicateError(RepositoryError):
    pass


class NotFoundError(RepositoryError):
    pass


class MemoryRepository[K: Hashable, V](Singleton):
    _storage: dict[K, V]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._instance is None:
            cls._storage = {}

        return super().__new__(cls, *args, **kwargs)

    def push(self, key: K, value: V) -> None:
        if key in self._storage:
            raise DuplicateError(f"Record with {key=} already created")

        self._storage[key] = value

    def get(self, key: K) -> V:
        try:
            return self._storage[key]
        except KeyError as exc:
            raise NotFoundError(f"{key=} not exists in storage") from exc

    def update(self, key: K, value: V) -> None:
        if key not in self._storage:
            raise NotFoundError(f"{key=} not exists in storage")

        self._storage[key] = value

    def delete(self, key: K) -> None:
        try:
            del self._storage[key]
        except KeyError as exc:
            raise NotFoundError(f"{key=} not exists in storage") from exc
