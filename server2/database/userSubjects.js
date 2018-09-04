const Joi = require('joi')

const db = require('./base')

const userSubjectSchema = Joi.object().keys({
  id: Joi.string().length(22),
  created: Joi.date(),
  modified: Joi.date(),
  userId: Joi.string().length(22),
  subjectId: Joi.string().length(22),
})

async function listUserSubjects(userId) {
  const query = `
    SELECT *
    FROM users_subjects
    WHERE user_id = $user_id
    ORDER BY created DESC;
  `
  return db.list(query, { user_id: userId })
}

async function insertUserSubject(userId, subjectId) {
  const params = { user_id: userId, subject_id: subjectId }
  Joi.assert(params, userSubjectSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO users_subjects
    ( user_id,  subject_id)
    VALUES
    ($user_id, $subject_id)
    RETURNING *;
  `
  const data = await db.save(query, params)
  return data
}

async function deleteUserSubject(userId, subjectId) {
  const params = { user_id: userId, subject_id: subjectId }
  Joi.assert(params, userSubjectSchema.requiredKeys(Object.keys(params)))
  const query = `
    DELETE FROM users_subjects
    WHERE user_id = $user_id AND subject_id = $subject_id;
  `
  return db.save(query, params)
}

module.exports = { listUserSubjects, insertUserSubject, deleteUserSubject }
