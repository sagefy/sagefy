
import routes.next  # TODO-2 switch to direct imports
from database.user import get_user, set_learning_context
from conftest import user_id
from modules.util import convert_uuid_to_slug


def test_seq_next(db_conn, session):
  """
  Expect sequencer route to say where to go next.
  """

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  user = get_user(db_conn, {'id': user_id})
  set_learning_context(user, next={
    'method': 'DANCE',
    'path': '/s/unicorns'
  })
  code, response = routes.next.next_route(request)
  assert code == 200
  assert response['next']['method'] == 'DANCE'
  set_learning_context(user, next=None)


def test_seq_next_default(db_conn, session):
  """
  Expect sequencer route to say where to go next if no current state.
  """

  request = {
    'cookies': {'session_id': session},
    'db_conn': db_conn,
  }
  code, response = routes.next.next_route(request)
  assert code == 200
  assert response == {
    'next': {
      'method': 'GET',
      'path': '/s/users/{user_id}/subjects'.format(
        user_id=convert_uuid_to_slug(user_id)
      ),
    }
  }


def test_seq_next_401(db_conn, session):
  """
  Expect sequencer route to say where to go next if no current state.
  """

  request = {
    'db_conn': db_conn,
  }
  code, _ = routes.next.next_route(request)
  assert code == 401
