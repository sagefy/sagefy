from elasticsearch import Elasticsearch
from config import config

es = Elasticsearch(
    hosts=[{
        'host': config['es_host'],
        'port': config['es_port']
    }]
)
