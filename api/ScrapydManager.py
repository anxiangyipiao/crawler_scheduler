# api.py

from fastapi import APIRouter, HTTPException
from utils.datebases import RedisConnectionManager
from model.model import ScrapydClienModel


router = APIRouter()

# 上传 Scrapyd 地址到 Redis 的接口
@router.post("/add_scrapyd_client")
def add_scrapyd_client(client: ScrapydClienModel):
    """
    上传 Scrapyd 客户端信息到 Redis。
    """
    redis_client = RedisConnectionManager.get_connection(db=0)  # 使用默认数据库
    key = f"scrapyd_client:{client.url}:{client.port}"
    
    # 检查是否已存在
    if redis_client.exists(key):
        raise HTTPException(status_code=400, detail="Scrapyd client already exists")

    # 将 Scrapyd 客户端信息存储到 Redis
    redis_client.hmset(key, {"url": client.url, "port": client.port})
    
    return {"message": "Scrapyd client added successfully", "client": client.dict()}






