from flask import Blueprint  # , jsonify, request

search_routes = Blueprint('search', __name__, url_prefix='/api/search')


@search_routes.route('/', methods=['GET'])
def search():
    """TODO@
    Search for entities. Search, filter, sort, paginate.

    Entities:
    - User
    - Card, Unit, Set
    - Version
    - Topic, Post

    Parameters:
    - q: query string
    - skip: for pagination
    - limit: for pagination
    - order: created...
    - order_by: asc or dsc
    - Filters
        - kind: the kind of entity to search for (set, card, unit)
        - language: the language of the entity
        - user_id: contains entites from the user
    """

    pass
    # TODO@ outline function
