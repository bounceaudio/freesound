# pylint: disable=unused-argument
import json
import threading
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Generator
from urllib.parse import parse_qs, urlparse

import pytest

from .client import FreesoundClient


# pylint: disable=arguments-differ,invalid-name
class CallbackHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler that delegates response to a callback."""

    callback: Callable[[str, dict[str, list[str]]], tuple[int, dict[str, Any]]]

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query_params = parse_qs(parsed.query)

        status_code, response_data = self.__class__.callback(parsed.path, query_params)

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def log_message(self, _format: str, *args: Any) -> None:
        """Suppress log messages during tests."""


# pylint: enable=arguments-differ,invalid-name


@pytest.fixture
def http_server(
    request: pytest.FixtureRequest,
) -> Generator[tuple[str, type[CallbackHTTPRequestHandler]], Any, None]:
    """
    Pytest fixture that runs an HTTP server for the duration of a test.

    The test can access the handler class from the returned tuple to set
    the callback function dynamically.

    Returns a tuple of (base_url: str, handler_class: type[CallbackHTTPRequestHandler]).
    """

    # Default no-op callback
    def default_callback(
        _path: str, _params: dict[str, list[str]]
    ) -> tuple[int, dict[str, Any]]:
        return (200, {"count": 0, "results": []})

    # Set the default callback on the handler class
    CallbackHTTPRequestHandler.callback = default_callback

    # Start server on a free port
    server = HTTPServer(("localhost", 0), CallbackHTTPRequestHandler)
    port = server.server_port
    base_url = f"http://localhost:{port}"

    # Run server in a background thread
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    yield base_url, CallbackHTTPRequestHandler

    # Cleanup
    server.shutdown()
    server.server_close()


def _single_page_callback(
    _path: str, _params: dict[str, list[str]]
) -> tuple[int, dict[str, Any]]:
    return (
        200,
        {
            "count": 2,
            "results": [
                {
                    "id": 123,
                    "name": "test_sound_1.wav",
                    "tags": ["test", "sound"],
                    "license": "CC BY 3.0",
                    "username": "testuser1",
                },
                {
                    "id": 456,
                    "name": "test_sound_2.wav",
                    "tags": ["ambient", "nature"],
                    "license": "CC0",
                    "username": "testuser2",
                },
            ],
        },
    )


# pylint: disable=redefined-outer-name
def test_text_search_single_page(
    http_server: tuple[str, type[CallbackHTTPRequestHandler]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test text search with a single page of results."""
    base_url, handler_class = http_server
    monkeypatch.setenv("FREESOUND_APIV2_TOKEN", "test_token")

    # Set callback for this test
    handler_class.callback = _single_page_callback

    client = FreesoundClient(base_url=base_url)
    results = list(client.text_search("test query", max_pages=1))

    assert len(results) == 2

    assert results[0].id == 123
    assert results[0].name == "test_sound_1.wav"
    assert results[0].tags == ["test", "sound"]
    assert results[0].license == "CC BY 3.0"
    assert results[0].username == "testuser1"

    assert results[1].id == 456
    assert results[1].name == "test_sound_2.wav"
    assert results[1].tags == ["ambient", "nature"]
    assert results[1].license == "CC0"
    assert results[1].username == "testuser2"


def test_text_search_multiple_pages(
    http_server: tuple[str, type[CallbackHTTPRequestHandler]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test text search with multiple pages of results."""
    base_url, handler_class = http_server
    monkeypatch.setenv("FREESOUND_APIV2_TOKEN", "test_token")

    # Track requests
    requests_made: list[tuple[str, dict[str, list[str]]]] = []

    def tracking_callback(
        path: str, params: dict[str, list[str]]
    ) -> tuple[int, dict[str, Any]]:
        requests_made.append((path, params))
        # Return one result per page
        return (
            200,
            {
                "count": 3,
                "results": [
                    {
                        "id": len(requests_made),
                        "name": f"sound_{len(requests_made)}.wav",
                        "tags": ["tag"],
                        "license": "CC BY 3.0",
                        "username": "user",
                    }
                ],
            },
        )

    # Inject callback for this test
    handler_class.callback = tracking_callback

    client = FreesoundClient(base_url=base_url)
    results = list(client.text_search("test", max_pages=3))

    assert len(results) == 3
    assert len(requests_made) == 3
    assert all(result.id == idx + 1 for idx, result in enumerate(results))


def _empty_results_callback(
    _path: str, _params: dict[str, list[str]]
) -> tuple[int, dict[str, Any]]:
    return (200, {"count": 0, "results": []})


def test_text_search_empty_results(
    http_server: tuple[str, type[CallbackHTTPRequestHandler]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test text search with no results."""
    base_url, handler_class = http_server
    monkeypatch.setenv("FREESOUND_APIV2_TOKEN", "test_token")

    # Set callback for this test
    handler_class.callback = _empty_results_callback

    client = FreesoundClient(base_url=base_url)
    results = list(client.text_search("nonexistent", max_pages=1))

    assert len(results) == 0


def test_text_search_validates_query_params(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the client sends the token parameter."""
    monkeypatch.setenv("FREESOUND_APIV2_TOKEN", "test_token_123")

    captured_params: dict[str, list[str]] = {}
    captured_path: list[str] = []

    def capture_callback(
        path: str, params: dict[str, list[str]]
    ) -> tuple[int, dict[str, Any]]:
        captured_path.append(path)
        captured_params.update(params)
        return (200, {"count": 0, "results": []})

    CallbackHTTPRequestHandler.callback = capture_callback

    # Start server manually for this test
    server = HTTPServer(("localhost", 0), CallbackHTTPRequestHandler)
    port = server.server_port
    base_url = f"http://localhost:{port}"

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        client = FreesoundClient(base_url=base_url)
        list(client.text_search("my search query", max_pages=1))

        # Verify correct endpoint is called
        assert captured_path[0] == "/search/text"
        # Verify token is sent
        assert captured_params.get("token") == ["test_token_123"]
    finally:
        server.shutdown()
        server.server_close()


def test_freesound_client_uses_env_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that FreesoundClient reads token from environment variable."""
    test_token = "env_token_456"
    monkeypatch.setenv("FREESOUND_APIV2_TOKEN", test_token)

    captured_token: list[str] = []

    def token_callback(
        _path: str, params: dict[str, list[str]]
    ) -> tuple[int, dict[str, Any]]:
        if "token" in params:
            captured_token.extend(params["token"])
        return (200, {"count": 0, "results": []})

    CallbackHTTPRequestHandler.callback = token_callback

    # Start server manually for this test
    server = HTTPServer(("localhost", 0), CallbackHTTPRequestHandler)
    port = server.server_port
    base_url = f"http://localhost:{port}"

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        client = FreesoundClient(base_url=base_url)
        list(client.text_search("test", max_pages=1))

        assert captured_token[0] == test_token
    finally:
        server.shutdown()
        server.server_close()


def test_freesound_client_requires_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that FreesoundClient requires FREESOUND_APIV2_TOKEN environment variable."""
    monkeypatch.delenv("FREESOUND_APIV2_TOKEN", raising=False)

    with pytest.raises(KeyError):
        FreesoundClient()


# pylint: enable=redefined-outer-name
