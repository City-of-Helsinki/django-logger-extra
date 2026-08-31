import logging
import uuid
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from logger_extra.apps import LIB_NAME
from logger_extra.logger_context import logger_context

logger = logging.getLogger(LIB_NAME)
GetResponseFn = Callable[[HttpRequest], HttpResponse]


class RequestIdMiddlewareBase:
    request_header: str
    response_header: str
    get_response: GetResponseFn

    def __init__(
        self,
        request_header: str,
        response_header: str,
        get_response: GetResponseFn,
    ):
        self.request_header = request_header
        self.response_header = response_header
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request_id = request.headers.get(self.request_header)

        if not request_id:
            request_id = str(uuid.uuid4())
            logger.error(
                "Request is missing %s header, using generated one instead.",
                self.request_header,
                extra={
                    "path": request.path,
                    "method": request.method,
                    "header_name": self.request_header,
                    "generated_id": request_id,
                },
            )

        with logger_context({"request_id": request_id}):
            response = self.get_response(request)
            response[self.response_header] = request_id

        return response


class XRequestIdMiddleware(RequestIdMiddlewareBase):
    header_name = "X-Request-ID"

    def __init__(self, get_response):
        super().__init__(self.header_name, self.header_name, get_response)
