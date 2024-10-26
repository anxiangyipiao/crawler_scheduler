# main.py

from fastapi import FastAPI
from api import router

app = FastAPI()

# 包含 API 路由
app.include_router(router)

# 启动 FastAPI 应用
# 在命令行中运行： uvicorn main:app --reload
