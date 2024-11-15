import json
from collections.abc import Awaitable, Callable
from dataclasses import asdict
from typing import Any

from src.handlers.http.api.register_user import register_user


async def app(
    scope: dict[str, Any],
    receive: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    body = None
    status = None
    if scope["type"] == "http" and scope["method"] == "POST" and scope["path"] == "/api/users":
        data = await receive()
        status, response = register_user(data)
        body = json.dumps(asdict(response)).encode("utf-8")

    await send(
        {
            "type": "http.response.start",
            "status": status or 200,
            "headers": [
                (b"content-type", b"application/json"),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body or b"{}"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
