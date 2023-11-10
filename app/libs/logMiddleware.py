import json

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.libs.logger import logger


class asyncIteratorWrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def setBody(self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(self, request, call_next):
        await self.setBody(request)

        try:
            requestBody = await request.json()
        except:
            requestBody = ""

        response = await call_next(request)

        responseBody = [section async for section in response.__dict__["body_iterator"]]
        response.__setattr__("body_iterator", asyncIteratorWrapper(responseBody))

        try:
            responseBody = json.loads(responseBody[0].decode())
        except:
            responseBody = str(responseBody)

        logger.info(
            "Incoming Request",
            extra={
                "req": {
                    "method": request.method,
                    "url": str(request.url),
                    "params": str(request.path_params),
                    "query": str(request.query_params),
                    "body": requestBody,
                },
                "res": {
                    "status": response.status_code,
                    "body": responseBody,
                },
            },
        )

        return response
