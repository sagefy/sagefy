from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=[{'host': 'elasticsearch', 'port': 9200}]
)
