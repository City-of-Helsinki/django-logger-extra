import logging
from collections.abc import Callable

import pytest

from logger_extra.apps import LIB_NAME
from logger_extra.filter import LoggerContextFilter
from tests.views import VIEWS_LOGGER_NAME

DUMMY_LOGGER_NAME = "dummy_middleware"


@pytest.fixture(scope="module", autouse=True)
def setup_dummy_middleware_logger():
    logger = logging.getLogger(DUMMY_LOGGER_NAME)
    logger.addFilter(LoggerContextFilter())
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)


def dummy_middleware(get_response):
    logger = logging.getLogger(DUMMY_LOGGER_NAME)

    def middleware(request):
        logger.info("dummy_middleware says hi")
        response = get_response(request)
        return response

    return middleware


def extract_logger_messages(
    caplog, predicate: Callable[[logging.LogRecord], bool]
) -> logging.LogRecord:
    return [r for r in caplog.records if predicate(r)]


def test_add_context_to_middleware_logs(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
        "tests.test_middleware.dummy_middleware",
    ]

    client.get("/nop")

    records = extract_logger_messages(caplog, lambda r: r.name == DUMMY_LOGGER_NAME)
    assert len(records) == 1
    record = records[0]
    assert record.name == "dummy_middleware"
    assert record.request_id


def test_generate_request_id_if_not_set(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
        "tests.test_middleware.dummy_middleware",
    ]

    client.get("/hello")

    records = extract_logger_messages(caplog, lambda r: r.name == DUMMY_LOGGER_NAME)
    assert len(records) == 1
    record = records[0]
    assert record.request_id


def test_use_request_id_from_header(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    client.get("/hello", headers={"X-Request-ID": "foo"})

    records = extract_logger_messages(caplog, lambda r: r.name == VIEWS_LOGGER_NAME)
    assert len(records) == 1
    record = records[0]
    assert record.request_id == "foo"


def test_add_logger_context_in_log_record(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    client.get("/parrot", {"foo": "bar"}, headers={"X-Request-ID": "foo"})

    records = extract_logger_messages(caplog, lambda r: r.name == VIEWS_LOGGER_NAME)
    assert len(records) == 1
    record = records[0]
    assert record.request_id == "foo"
    assert record.foo == "bar"


def test_logger_context_ignores_builtins(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    client.get("/parrot", {"message": "overridden"})

    records = extract_logger_messages(caplog, lambda r: r.name == VIEWS_LOGGER_NAME)
    assert len(records) == 1
    record = records[0]
    assert record.request_id
    assert record.message != "overridden"


def test_request_id_is_logged_on_error(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    with pytest.raises(ValueError):
        client.get("/error", headers={"X-Request-ID": "foo"})

    exceptions = extract_logger_messages(caplog, lambda r: r.exc_info is not None)
    assert len(exceptions) == 1
    record = exceptions[0]
    assert record.request_id == "foo"


def test_missing_header_triggers_error_log(caplog, client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    client.get("/hello")

    records = extract_logger_messages(caplog, lambda r: r.name == LIB_NAME)
    assert len(records) == 1

    record = records[0]
    assert "missing X-Request-ID header" in record.message

    assert record.header_name == "X-Request-ID"
    assert record.generated_id is not None


def test_response_contains_request_id_header(client, settings):
    settings.MIDDLEWARE = [
        "logger_extra.middleware.XRequestIdMiddleware",
    ]

    response = client.get("/hello", headers={"X-Request-ID": "test-id-123"})
    assert response["X-Request-ID"] == "test-id-123"

    response = client.get("/hello")
    assert "X-Request-ID" in response
    assert len(response["X-Request-ID"]) > 0
