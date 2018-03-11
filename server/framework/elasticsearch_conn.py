from config import config
from elasticsearch import Elasticsearch

es = Elasticsearch(
  hosts=[{
    'host': config['es_host'],
    'port': config['es_port']
  }]
)
