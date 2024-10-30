# main.py

from fastapi import Depends, FastAPI,Request
from crawler_scheduler.api import auth_api,scrapyd_api,system_info_api,schedule_api,stats_collection_api,scrapyd_server_api
from fastapi.responses import JSONResponse
from crawler_scheduler.service.auth_service import AuthService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(default_response_class=JSONResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名跨域
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

# 引入中间件
def check_token(request: Request, call_next):
    token = request.headers.get('Token')
    AuthService.check_token(token)
    response = call_next(request)
    return response


# 包含 API 路由
app.include_router(auth_api, tags=["auth_api"],prefix='/auth')
app.include_router(scrapyd_api, tags=["scrapyd_api"])
app.include_router(system_info_api, tags=["system_info_api"])
app.include_router(schedule_api, tags=["schedule_api"])
app.include_router(stats_collection_api, tags=["stats_collection_api"])
app.include_router(scrapyd_server_api, tags=["scrapyd_server_api"])



# 启动 FastAPI 应用
# 在命令行中运行： uvicorn main:app --reload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=18000)