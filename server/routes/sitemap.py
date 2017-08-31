from framework.routes import get
from database.user import list_users, deliver_user
from database.topic import list_topics
from database.card import list_all_card_entity_ids
from database.unit import list_all_unit_entity_ids
from database.subject import list_all_subject_entity_ids


defaults = {
    'https://sagefy.org/',
    'https://sagefy.org/sign_up',
    'https://sagefy.org/log_in',
    'https://sagefy.org/password',
    'https://sagefy.org/terms',
    'https://sagefy.org/contact',
    'https://sagefy.org/search',
}


@get('/s/sitemap.txt')
def sitemap_route(request):
    """
    Generate a sitemap so Google can find Sagefy's content.
    Should be linked to from https://sagefy.org/robots.txt
    Sitemap: https://sagefy.org/s/sitemap.txt
    """

    # TODO-1 cache in redis
    db_conn = request['db_conn']
    sitemap = defaults | set()
    # Card, unit, subject
    kinds = {
        'cards': list_all_card_entity_ids(db_conn),
        'units': list_all_unit_entity_ids(db_conn),
        'subjects': list_all_subject_entity_ids(db_conn),
    }
    for tablename, entity_ids in kinds.items():
        for entity_id in entity_ids:
            sitemap.add('https://sagefy.org/{tablename}/{id}'.format(
                id=entity_id,
                kind=tablename[:-1],
            ))
            # TODO-2 ...and versions pages
    # Topic
    for topic in list_topics(db_conn, {}):
        sitemap.add('https://sagefy.org/topics/{id}'.format(id=topic['id']))
    # User
    users = [deliver_user(user) for user in list_users(db_conn, {})]
    for user in users:
        sitemap.add('https://sagefy.org/users/{id}'.format(id=user['id']))
    sitemap = '\n'.join(sitemap)
    return 200, sitemap
