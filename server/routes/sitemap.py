from framework.routes import get
from models.card import Card
from models.unit import Unit
from models.subject import Subject
from database.user import list_users, deliver_user
from database.topic import list_topics

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
    kinds = {'card': Card, 'unit': Unit, 'subject': Subject}
    for kind, Model in kinds.items():
        query = Model.start_accepted_query()
        entities = [Model(data).deliver() for data in query.run(db_conn)]
        for entity in entities:
            sitemap.add('https://sagefy.org/{kind}s/{id}'.format(
                id=entity['entity_id'],
                kind=kind
            ))
            # TODO-2 ...and versions pages
            # TODO-2

    # Topic
    for topic in list_topics({}, db_conn):
        sitemap.add('https://sagefy.org/topics/{id}'.format(id=topic['id']))

    # User
    users = [deliver_user(user) for user in list_users({}, db_conn)]
    for user in users:
        sitemap.add('https://sagefy.org/users/{id}'.format(id=user['id']))

    sitemap = '\n'.join(sitemap)
    return 200, sitemap
