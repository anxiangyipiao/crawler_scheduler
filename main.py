# main.py

from fastapi import Depends, FastAPI,Request
from crawler_scheduler.api import auth_api,scrapyd_api
from fastapi.responses import JSONResponse
from crawler_scheduler.service.auth_service import AuthService


app = FastAPI(default_response_class=JSONResponse)


# 引入中间件
def check_token(request: Request, call_next):
    token = request.headers.get('Token')
    AuthService.check_token(token)
    response = call_next(request)
    return response


# 包含 API 路由
app.include_router(auth_api, tags=["auth_api"])
app.include_router(scrapyd_api, tags=["scrapyd_api"], dependencies=[Depends(check_token)])


# 启动 FastAPI 应用
# 在命令行中运行： uvicorn main:app --reload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=18000)