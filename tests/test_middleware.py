import logging
import uuid

import pytest

from logger_extra.filter import LoggerContextFilter


@pytest.fixture(scope="module", autouse=True)
def setup_dummy_middleware_logger():
    logger = logging.getLogger("dummy_middleware")
    logger.addFilter(LoggerContextFilter())
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)


def dummy_middleware(get_response):
    logger = logging.getLogger("dummy_middleware")

    def middleware(request):
        logger.info("dummy_middleware says hi")
        response = get_response(request)
        return response

    return middleware


def test_add_context_to_middleware_logs(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
        "tests.test_middleware.dummy_middleware",
    ]

    client.get("/nop")

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.name == "dummy_middleware"
    assert record.request_id


def test_generate_request_id_if_not_set(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    client.get("/hello")

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.request_id


def test_use_request_id_from_header(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    client.get("/hello", headers={"X-Request-ID": "foo"})

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.request_id == "foo"


def test_add_logger_context_in_log_record(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    client.get("/parrot", {"foo": "bar"})

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.request_id
    assert record.foo == "bar"


def test_logger_context_ignores_builtins(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    client.get("/parrot", {"message": "overridden"})

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.request_id
    assert record.message != "overridden"


def test_request_id_is_logged_on_error(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    with pytest.raises(ValueError):
        client.get("/error", headers={"X-Request-ID": "foo"})

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.request_id == "foo"


def test_request_id_valid_formats(caplog, client, settings):
    """
    Ensure standard identifiers (UUID, MD5, SHA256) are accepted as-is.
    """
    settings.MIDDLEWARE = ["logger_extra.middleware.XRequestIdMiddleware"]

    valid_ids = [
        str(uuid.uuid4()),  # UUID v4
        "098f6bcd4621d373cade4e832627b4f6",  # MD5
        "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",  # SHA256
        "trace_id_123-abc",  # Alphanumeric with hyphens and underscores
    ]

    for valid_id in valid_ids:
        caplog.clear()
        client.get("/hello", headers={"X-Request-ID": valid_id})

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.request_id == valid_id


def test_reject_invalid_request_id_characters(caplog, client, settings):
    """
    Ensure header values containing control characters,
    quotes, or invalid symbols are rejected.
    """
    settings.MIDDLEWARE = ["logger_extra.middleware.XRequestIdMiddleware"]

    invalid_ids = [
        'bad"id',  # Double quotes
        "bad'id",  # Single quotes
        "bad\nid",  # Embedded newline
        "bad\rid",  # Embedded carriage return
        "bad id",  # Space
        "bad<script>",  # HTML/XML tags
        "bad/id",  # Forward slash
    ]

    for invalid_id in invalid_ids:
        caplog.clear()
        client.get("/hello", headers={"X-Request-ID": invalid_id})

        assert len(caplog.records) == 1
        record = caplog.records[0]
        # Should drop the header and generate a new UUID
        assert record.request_id != invalid_id
        assert uuid.UUID(record.request_id)  # Verifies it fell back to a valid UUID


def test_reject_oversized_request_id(caplog, client, settings):
    """Ensure request IDs exceeding length bounds (64 chars) are rejected."""
    settings.MIDDLEWARE = ["logger_extra.middleware.XRequestIdMiddleware"]

    oversized_id = "a" * 65

    client.get("/hello", headers={"X-Request-ID": oversized_id})

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.request_id != oversized_id
    assert uuid.UUID(record.request_id)


def test_reject_trailing_newline_request_id(caplog, client, settings):
    """Ensure trailing newlines fail regex match and generate a fresh UUID."""
    settings.MIDDLEWARE = ["logger_extra.middleware.XRequestIdMiddleware"]

    id_with_newline = "valid-id\n"

    client.get("/hello", headers={"X-Request-ID": id_with_newline})

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.request_id != id_with_newline
    assert uuid.UUID(record.request_id)
