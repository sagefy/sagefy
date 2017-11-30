import uuid
from database.entity_base import save_entity_to_es


def test_save_entity_to_es():
  kind = 'unit'
  data = {
    'status': 'accepted',
    'entity_id': uuid.uuid4(),
  }
  assert save_entity_to_es(kind, data)
