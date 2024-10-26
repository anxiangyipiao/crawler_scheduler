# api.py

from fastapi import APIRouter, HTTPException
from model.model import ScrapydClienModel
from utils import redis_client



ScrapydRouter = APIRouter()

# 上传 Scrapyd 地址到 Redis 的接口
@ScrapydRouter.post("/add_scrapyd_client")
def add_scrapyd_client(client: ScrapydClienModel):
    """
    上传 Scrapyd 客户端信息到 Redis。
    """
    key = f"scrapyd_client:{client.url}:{client.port}"
    
    # 检查是否已存在
    if redis_client.exists(key):
        raise HTTPException(status_code=400, detail="Scrapyd client already exists")

    # 将 Scrapyd 客户端信息存储到 Redis
    redis_client.hmset(key, {"url": client.url, "port": client.port})
    

    return {"message": "Scrapyd client added successfully", "client": client.dict()}


# 获取所有 Scrapyd 客户端信息的接口
@ScrapydRouter.get("/get_scrapyd_clients")
def get_scrapyd_clients():
    """
    获取所有 Scrapyd 客户端信息。
    """
    keys = redis_client.keys("scrapyd_client:*")
    clients = []
    for key in keys:
        data = redis_client.hgetall(key)
        clients.append({k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()})
    return clients


# 删除 Scrapyd 客户端信息的接口
@ScrapydRouter.delete("/delete_scrapyd_client")
def delete_scrapyd_client(client: ScrapydClienModel):
    """
    删除 Scrapyd 客户端信息。
    """
    key = f"scrapyd_client:{client.url}:{client.port}"
    result = redis_client.delete(key)
    if not result:
        raise HTTPException(status_code=404, detail="Scrapyd client not found")
    return {"message": "Scrapyd client deleted successfully"}
