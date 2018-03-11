import uuid
from framework.redis_conn import red
from database.user import get_user  # pylint: disable=E0611
from modules.util import convert_uuid_to_slug


def get_current_user(request):
  """
  Get the current user if available, else None.
  """

  cookies = request.get('cookies', {})
  session_id = cookies.get('session_id')
  user_id = red.get(session_id)
  db_conn = request['db_conn']
  if user_id:
    user_id = user_id.decode()
    return get_user(db_conn, {'id': user_id})


def log_in_user(user):
  """
  Log in the given user.
  """

  session_id = convert_uuid_to_slug(uuid.uuid4())
  red.setex(
    session_id,
    2 * 7 * 24 * 60 * 60,
    convert_uuid_to_slug(user['id']),
  )
  return session_id


def log_out_user(request):
  """
  Log out the given user.
  """

  cookies = request.get('cookies', {})
  session_id = cookies.get('session_id')
  if session_id:
    red.delete(session_id)
