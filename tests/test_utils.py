import datetime
from socket import socket

import pytest
from django.test import RequestFactory

from logger_extra.utils import json_serialize


@pytest.mark.parametrize(
    "value,expected",
    [
        (datetime.datetime.min, datetime.datetime.min.isoformat()),
        (datetime.date.min, datetime.date.min.isoformat()),
        (
            RequestFactory().get("/foo"),
            {
                "source": "http",
                "method": "GET",
                "path": "/foo",
            },
        ),
    ],
)
def test_json_serialize_handled_cases(value, expected):
    assert json_serialize(value) == expected


def test_json_serialize_socket(monkeypatch):
    monkeypatch.setattr(socket, "getsockname", lambda *_, **__: "sockname")
    monkeypatch.setattr(socket, "getpeername", lambda *_, **__: "peername")

    assert json_serialize(socket()) == {
        "source": "socket",
        "socket": "sockname",
        "peer": "peername",
    }


def test_json_serialize_defaults_to_str():
    class Foo:
        def __str__(self) -> str:
            return "hello world"

    assert json_serialize(Foo()) == "hello world"
