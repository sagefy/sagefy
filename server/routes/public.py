from framework.routes import get
from modules.content import get as c


@get('/s')
def index_route(request):
  """
  View a documentation page.
  """

  return 200, {'message': c('welcome')}
