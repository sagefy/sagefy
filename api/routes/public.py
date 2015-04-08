from framework.index import get
from modules.content import get as c


@get('/api')
def index_route(request):
    """
    View a documentation page.
    """

    return 200, {'message': c('api', 'welcome')}
