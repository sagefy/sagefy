from config import config
from redis import StrictRedis

red = StrictRedis(
  host=config['redis_host'],
  port=config['redis_port']
)
