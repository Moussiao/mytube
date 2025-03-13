from typing import Any, Self


class Singleton:
    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance
