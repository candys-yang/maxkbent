'''
初始化 redis
'''
import redis
from . import config

class Base: 
    ''' 基础对象 '''
    def __init__(self) -> None:
        self.pool = redis.ConnectionPool.from_url(
            config.Database().redis
        )
        
    def Create_Client(self): 
        ''' 创建 Redis 连接对象 '''
        self.client = redis.Redis(
            connection_pool=self.pool, decode_responses=True)
        return self.client
    