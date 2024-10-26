# main.py

from fastapi import FastAPI
from crawler_scheduler.api import auth_api,scrapyd_api

app = FastAPI()

# 包含 API 路由
app.include_router(auth_api, tags=["auth_api"])
app.include_router(scrapyd_api, tags=["scrapyd_api"])

# 启动 FastAPI 应用
# 在命令行中运行： uvicorn main:app --reload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=18000)