import asyncio
import json
from collections.abc import Generator
from typing import Any
from urllib.parse import urlsplit

import pytest
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.dependencies import get_db
from app.main import app
from app.models import Item

TEST_DATABASE_URL = "sqlite://"


class ASGITestClient:
    def __init__(self, app) -> None:
        self.app = app
        self.base_url = "http://testserver"

    def __enter__(self) -> "ASGITestClient":
        asyncio.run(self.app.router.startup())
        return self

    def __exit__(self, *args: Any) -> None:
        asyncio.run(self.app.router.shutdown())

    def request(
        self,
        method: str,
        path: str,
        json_body: Any = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        target = path if "://" in path else f"{self.base_url}{path}"
        parsed = urlsplit(target)
        body = b""
        request_headers = [(b"host", (parsed.netloc or "testserver").encode("ascii"))]

        if headers:
            for name, value in headers.items():
                request_headers.append((name.lower().encode("ascii"), value.encode("ascii")))

        if json_body is not None:
            body = json.dumps(json_body).encode("utf-8")
            request_headers.append((b"content-type", b"application/json"))

        async def run_request() -> list[dict[str, Any]]:
            messages: list[dict[str, Any]] = []
            request_sent = False

            async def receive() -> dict[str, Any]:
                nonlocal request_sent
                if not request_sent:
                    request_sent = True
                    return {"type": "http.request", "body": body, "more_body": False}
                return {"type": "http.disconnect"}

            async def send(message: dict[str, Any]) -> None:
                messages.append(message)

            scope = {
                "type": "http",
                "asgi": {"version": "3.0", "spec_version": "2.3"},
                "http_version": "1.1",
                "method": method.upper(),
                "scheme": parsed.scheme or "http",
                "path": parsed.path or "/",
                "raw_path": (parsed.path or "/").encode("ascii"),
                "query_string": parsed.query.encode("ascii"),
                "headers": request_headers,
                "client": ("testclient", 50000),
                "server": (parsed.hostname or "testserver", parsed.port or 80),
                "root_path": "",
                "state": {},
            }

            await self.app(scope, receive, send)
            return messages

        messages = asyncio.run(run_request())
        status_code = 500
        response_headers: list[tuple[str, str]] = []
        response_body = bytearray()

        for message in messages:
            if message["type"] == "http.response.start":
                status_code = message["status"]
                response_headers = [
                    (key.decode("latin-1"), value.decode("latin-1"))
                    for key, value in message.get("headers", [])
                ]
            elif message["type"] == "http.response.body":
                response_body.extend(message.get("body", b""))

        request = httpx.Request(method.upper(), target, content=body)
        return httpx.Response(
            status_code=status_code,
            headers=dict(response_headers),
            content=bytes(response_body),
            request=request,
        )

    def get(self, path: str) -> httpx.Response:
        return self.request("GET", path)

    def post(self, path: str, json: Any | None = None) -> httpx.Response:
        return self.request("POST", path, json_body=json)

    def options(
        self,
        path: str,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        return self.request("OPTIONS", path, headers=headers)


@pytest.fixture
def session_factory() -> Generator[sessionmaker, None, None]:
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    factory = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    yield factory

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def client(
    session_factory: sessionmaker,
) -> Generator[ASGITestClient, None, None]:
    async def override_get_db_session() -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db_session

    with ASGITestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
