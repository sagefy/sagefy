from config import config
from elasticsearch import Elasticsearch  # pylint: disable=W0406

es = Elasticsearch(  # pylint: disable=C0103
  hosts=[{
    'host': config['es_host'],
    'port': config['es_port']
  }]
)
