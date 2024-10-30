from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable
from crawler_scheduler.utils.api_result import ApiResult

# 返回统一的api格式

class ApiResultMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)
        if response.status_code == 200:
            data = response.body
            response.body = ApiResult.success(data=data).json()
        elif response.status_code != 200 and response.status_code != 403:
            data = response.body
            response.body = ApiResult.failure(data=data).json()
        
        return response



