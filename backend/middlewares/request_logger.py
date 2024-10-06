import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self
            , app
            , log_level=logging.INFO
            , is_request_logging_on=True
        ):
        super().__init__(app)
        self.log_level = log_level
        self.is_request_logging_on = is_request_logging_on
    async def dispatch(self, request: Request, call_next):
        if self.is_request_logging_on:
            logging.info(f"Incoming request: {request.method} {request.url}")
            logging.info(f"Request headers: {request.headers}")
            response = await call_next(request)
            return response
        else:
            return await call_next(request)