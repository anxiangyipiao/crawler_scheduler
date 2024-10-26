# main.py

from fastapi import FastAPI
from api import ScrapydRouter,UserRouter

app = FastAPI()

# 包含 API 路由
app.include_router(ScrapydRouter, tags=["Scrapyd"])
app.include_router(UserRouter, tags=["User"])

# 启动 FastAPI 应用
# 在命令行中运行： uvicorn main:app --reload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=18000)