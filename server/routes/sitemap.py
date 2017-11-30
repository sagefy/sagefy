from framework.routes import get
from database.user import list_users, deliver_user
from database.topic import list_topics
from database.card import list_all_card_entity_ids
from database.unit import list_all_unit_entity_ids
from database.subject import list_all_subject_entity_ids
from modules.util import convert_uuid_to_slug


DEFAULTS = {
  'https://sagefy.org/',
  'https://sagefy.org/sign_up',
  'https://sagefy.org/log_in',
  'https://sagefy.org/password',
  'https://sagefy.org/terms',
  'https://sagefy.org/contact',
  'https://sagefy.org/search',
}


@get('/s/sitemap.txt')
def get_sitemap_route(request):
  """
  Generate a sitemap so Google can find Sagefy's content.
  Should be linked to from https://sagefy.org/robots.txt
  Sitemap: https://sagefy.org/s/sitemap.txt
  """

  # TODO-1 cache in redis
  db_conn = request['db_conn']
  sitemap = DEFAULTS | set()
  # Card, unit, subject
  kinds = {
    'card': list_all_card_entity_ids(db_conn),
    'unit': list_all_unit_entity_ids(db_conn),
    'subject': list_all_subject_entity_ids(db_conn),
  }
  for kind, entity_ids in kinds.items():
    for entity_id in entity_ids:
      sitemap.add(
        'https://sagefy.org/{kind}s/{id}'.format(
          id=convert_uuid_to_slug(entity_id),
          kind=kind,
        )
      )
      # TODO-2 ...and versions pages
  # Topic
  for topic in list_topics(db_conn, {}):
    sitemap.add(
      'https://sagefy.org/topics/{id}'.format(
        id=convert_uuid_to_slug(topic['id'])
      )
    )
  # User
  users = [deliver_user(user) for user in list_users(db_conn, {})]
  for user in users:
    sitemap.add(
      'https://sagefy.org/users/{id}'.format(
        id=convert_uuid_to_slug(user['id'])
      )
    )
  sitemap = '\n'.join(sitemap)
  return 200, sitemap
