from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, slots=True)
class User:
    id: int
    username: str
    password: str
