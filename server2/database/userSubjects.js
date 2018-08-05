const Joi = require('joi')

const db = require('./index')

const userSubjectSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  userId: Joi.string().guid(),
  subjectId: Joi.string().guid(),
})

/*
insert_user_subject
  query = """
    INSERT INTO users_subjects
    (  user_id  ,   subject_id  )
    VALUES
    (%(user_id)s, %(subject_id)s)
    RETURNING *;
  """

list_user_subjects
  query = """
    SELECT *
    FROM users_subjects
    WHERE user_id = %(user_id)s
    ORDER BY created DESC;
  """

remove_user_subject
  query = """
    DELETE FROM users_subjects
    WHERE user_id = %(user_id)s AND subject_id = %(subject_id)s;
  """
*/

async function listUserSubjects(userId) {}

async function insertUserSubject(userId, subjectId) {}

async function deleteUserSubject(userId, subjectId) {}

module.exports = { listUserSubjects, insertUserSubject, deleteUserSubject }
