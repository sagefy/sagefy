from redis import StrictRedis
from config import config

redis = StrictRedis(
    host=config['redis_host'],
    port=config['redis_port']
)
