import re
import uuid
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from logger_extra.logger_context import logger_context

GetResponseFn = Callable[[HttpRequest], HttpResponse]


class RequestIdMiddlewareBase:
    request_header: str
    response_header: str
    get_response: GetResponseFn

    # Safe characters only, reasonable length bounds (1-64 chars)
    _REQUEST_ID_RE = re.compile(r"^[a-zA-Z0-9\-_]{1,64}$")

    def __init__(
        self,
        request_header: str,
        response_header: str,
        get_response: GetResponseFn,
    ):
        self.request_header = request_header
        self.response_header = response_header
        self.get_response = get_response

    def _get_or_generate_request_id(self, request: HttpRequest) -> str:
        header_value = request.headers.get(self.request_header)

        if header_value and self._REQUEST_ID_RE.match(header_value):
            return header_value

        return str(uuid.uuid4())

    def __call__(self, request: HttpRequest):
        request_id = self._get_or_generate_request_id(request)

        with logger_context({"request_id": request_id}):
            response = self.get_response(request)
            response[self.response_header] = request_id

        return response


class XRequestIdMiddleware(RequestIdMiddlewareBase):
    header_name = "X-Request-ID"

    def __init__(self, get_response):
        super().__init__(self.header_name, self.header_name, get_response)
