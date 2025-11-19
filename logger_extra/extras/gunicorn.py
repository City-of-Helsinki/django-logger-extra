import datetime
import json
import logging

from logger_extra.utils import json_serialize


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        response_time = datetime.datetime.strptime(
            record.args["t"], "[%d/%b/%Y:%H:%M:%S %z]"
        ).astimezone(datetime.timezone.utc)
        url = record.args["U"]
        if record.args["q"]:
            url += f"?{record.args['q']}"

        formatted = {
            "time": response_time.isoformat(),
            "source": "gunicorn.access",
            "remote_addr": record.args["h"],
            "x_forwarded_for": record.args["{x-forwarded-for}o"],
            "request_id": record.args["{x-request-id}o"],
            "remote_user": record.args["u"],
            "bytes_sent": record.args["B"],
            "request_time": record.args["L"],
            "status": record.args["s"],
            "host": record.args["{http_host}e"],
            "request_proto": record.args["H"],
            "request_method": record.args["m"],
            "path": url,
            "request_length": record.args["{content_length}e"],
            "http_referer": record.args["{http_referer}e"],
            "http_user_agent": record.args["a"],
        }

        return json.dumps(formatted, default=json_serialize)


class JsonErrorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        created_at = datetime.datetime.fromtimestamp(
            record.created, tz=datetime.timezone.utc
        )
        formatted = {
            "time": created_at.isoformat(),
            "source": "gunicorn.error",
            "message": record.getMessage(),
        }

        return json.dumps(formatted, default=json_serialize)
