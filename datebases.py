import redis
from redis import ConnectionPool


host = 'localhost'
port = 6379


class RedisConnectionManager:
    _pool = None

    @classmethod
    def get_pool(cls,db):
        if cls._pool is None:
            cls._pool = ConnectionPool(host=host, port=port, db=db)
        return cls._pool


    @classmethod
    def get_connection(cls,db):
        return redis.Redis(connection_pool=cls.get_pool(db))