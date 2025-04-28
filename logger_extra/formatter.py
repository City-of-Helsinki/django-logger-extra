import json
from logging import LogRecord
from socket import socket
from typing import Any

from django.http import HttpRequest
from django.utils import timezone
from json_log_formatter import JSONFormatter as BaseJSONFormatter

from logger_extra.logger_context import get_logger_context


class JSONFormatter(BaseJSONFormatter):
    def json_record(self, message: str, extra: dict, record: LogRecord) -> dict:
        request = extra.pop('request', None)
        extra.pop('response', None)

        logger_context = get_logger_context()

        for key, value in logger_context.items():
            extra[key] = value

        if request:
            extra['request'] = self.format_request(request)

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        formatted = {
            'message': message,
            'level': record.levelname,
            'name': record.name,
            'time': timezone.now(),
            'context': extra,
        }

        return formatted

    def format_request(self, request: Any) -> str:
        if isinstance(request, socket):
            return json.dumps({
                "source": "socket",
                "socket": request.getsockname(),
                "peer": request.getpeername(),
            })

        if isinstance(request, HttpRequest):
            return json.dumps({
                "source": "http",
                "method": request.method,
                "path": request.path,
            })

        return str(request)
