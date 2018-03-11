from config import config
from redis import StrictRedis  # pylint: disable=W0406

red = StrictRedis(  # pylint: disable=C0103
  host=config['redis_host'],
  port=config['redis_port']
)
