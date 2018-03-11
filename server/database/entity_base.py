from framework.elasticsearch_conn import es
from modules.util import json_prep, convert_uuid_to_slug


def save_entity_to_es(kind, data):
  """
  Overwrite save method to add to Elasticsearch.
  """

  # NB use deliver_thing(entity) BEFORE calling this function
  body = json_prep(data)
  if data['status'] == 'accepted':
    return es.index(
      index='entity',
      doc_type=kind,
      body=body,
      id=convert_uuid_to_slug(data['entity_id']),
    )
