"""
Record the list of subjects the learner has added.
"""

from schemas.user_subjects import schema as user_subjects_schema
from database.util import insert_row, list_rows, delete_row
from database.subject import list_latest_accepted_subjects
from modules.util import convert_slug_to_uuid


def insert_user_subject(db_conn, user_id, subject_id):
  """
  Add a new user subjects entry to the database.
  """

  schema = user_subjects_schema
  query = """
    INSERT INTO users_subjects
    (  user_id  ,   subject_id  )
    VALUES
    (%(user_id)s, %(subject_id)s)
    RETURNING *;
  """
  data = {
    'user_id': convert_slug_to_uuid(user_id),
    'subject_id': convert_slug_to_uuid(subject_id),
  }
  data, errors = insert_row(db_conn, schema, query, data)
  return data, errors


def list_user_subjects(db_conn, user_id):
  """
  List the user subjects for a user from the database.
  """

  query = """
    SELECT *
    FROM users_subjects
    WHERE user_id = %(user_id)s
    ORDER BY created DESC;
    /* TODO OFFSET LIMIT */
  """
  params = {'user_id': convert_slug_to_uuid(user_id)}
  return list_rows(db_conn, query, params)


def remove_user_subject(db_conn, user_id, subject_id):
  """
  Remove a subject from a user's list of subjects.
  """

  query = """
    DELETE FROM users_subjects
    WHERE user_id = %(user_id)s AND subject_id = %(subject_id)s;
  """
  params = {
    'user_id': convert_slug_to_uuid(user_id),
    'subject_id': convert_slug_to_uuid(subject_id),
  }
  errors = delete_row(db_conn, query, params)
  return errors


def list_user_subjects_entity(db_conn, user_id, params):
  """
  Join the user's subject_ids with subject information.
  Return empty list when there's no matching documents.
  """

  # TODO-2 each subject -- needs review?
  # TODO-2 order by last reviewed time
  user_subjects = list_user_subjects(db_conn, user_id)
  # TODO-3 limit = params.get('limit') or 10
  # TODO-3 offset = params.get('offset') or 0
  subject_ids = [data['subject_id'] for data in user_subjects]
  return list_latest_accepted_subjects(db_conn, subject_ids)
