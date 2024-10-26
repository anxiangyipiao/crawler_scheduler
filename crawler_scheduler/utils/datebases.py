from redis import Redis
from redis import ConnectionPool



# Redis 连接管理器
class RedisConnectionManager:
    _pool = None

    @classmethod
    def get_pool(cls, db):
        if cls._pool is None:
            cls._pool = ConnectionPool(host='43.128.136.204', port=16379, db=db)
        return cls._pool

    @classmethod
    def get_connection(cls, db):
        return Redis(connection_pool=cls.get_pool(db))
    

# 创建 Redis 连接
try:
    redis_client = RedisConnectionManager.get_connection(db=1)  # 使用默认数据库
    redis_client.ping()
    print("Redis 连接成功")
except Exception as e:
    print(f"Redis 连接失败: {e}")

