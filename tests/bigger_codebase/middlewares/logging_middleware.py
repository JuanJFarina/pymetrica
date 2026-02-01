import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class logging_middleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        logging.info(f"Request URL: {request.url}")
        response = await call_next(request)
        logging.info(f"Response status code: {response.status_code}")
        return response
