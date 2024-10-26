from redis import Redis
from redis import ConnectionPool



# Redis 连接管理器
class RedisConnectionManager:
    _pool = None

    @classmethod
    def get_pool(cls, db):
        if cls._pool is None:
            cls._pool = ConnectionPool(host='localhost', port=6379, db=db)
        return cls._pool

    @classmethod
    def get_connection(cls, db):
        return Redis(connection_pool=cls.get_pool(db))