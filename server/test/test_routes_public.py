
import routes.public  # TODO-2 switch to direct imports


def test_welcome():
  """
  Ensure the server returns a welcome message.
  """

  code, response = routes.public.index_route({})
  assert code == 200
  assert 'Welcome' in response['message']
