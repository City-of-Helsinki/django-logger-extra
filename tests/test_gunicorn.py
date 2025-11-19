import logging
from collections import defaultdict

from freezegun import freeze_time

from logger_extra.extras.gunicorn import JsonErrorFormatter, JsonFormatter


def test_json_formatter():
    log_args = defaultdict(lambda: "-")
    log_args.update(
        {
            "t": "[31/Jan/2000:23:59:59 +03:00]",
            "h": "remote-addr",
            "{x-forwarded-for}o": "x-forwarded-for",
            "{x-request-id}o": "x-request-id",
            "u": "remote-user",
            "B": 123,
            "L": "request-time",
            "s": "status",
            "{http_host}e": "http-host",
            "H": "protocol",
            "m": "method",
            "U": "/foo",
            "q": "foo=bar&xyz=baz",
            "{content_length}e": 456,
            "{http_referer}e": "http-referer",
            "a": "user-agent",
        }
    )

    formatter = JsonFormatter()
    formatted = formatter.format(
        logging.LogRecord(
            name="test.json_access",
            level=logging.INFO,
            pathname="",
            lineno=1,
            msg="hello world",
            args=log_args,
            exc_info=None,
        )
    )

    assert (
        formatted == "{"
        '"time": "2000-01-31T20:59:59+00:00", '
        '"source": "gunicorn.access", '
        '"remote_addr": "remote-addr", '
        '"x_forwarded_for": "x-forwarded-for", '
        '"request_id": "x-request-id", '
        '"remote_user": "remote-user", '
        '"bytes_sent": 123, '
        '"request_time": "request-time", '
        '"status": "status", '
        '"host": "http-host", '
        '"request_proto": "protocol", '
        '"request_method": "method", '
        '"path": "/foo?foo=bar&xyz=baz", '
        '"request_length": 456, '
        '"http_referer": "http-referer", '
        '"http_user_agent": "user-agent"'
        "}"
    )


def test_json_error_formatter():
    formatter = JsonErrorFormatter()
    with freeze_time("2000-01-31 00:00:00"):
        formatted = formatter.format(
            logging.LogRecord(
                name="test.json_error",
                level=logging.INFO,
                pathname="",
                lineno=1,
                msg="hello world",
                args=None,
                exc_info=None,
            )
        )

    assert (
        formatted == "{"
        '"time": "2000-01-31T00:00:00+00:00", '
        '"source": "gunicorn.error", '
        '"message": "hello world"'
        "}"
    )
