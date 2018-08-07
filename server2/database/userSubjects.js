const Joi = require('joi')

const db = require('./index')

const userSubjectSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  userId: Joi.string().guid(),
  subjectId: Joi.string().guid(),
})

async function listUserSubjects(userId) {
  const query = `
    SELECT *
    FROM users_subjects
    WHERE user_id = $user_id
    ORDER BY created DESC;
  `
}

async function insertUserSubject(userId, subjectId) {
  const query = `
    INSERT INTO users_subjects
    ( user_id,  subject_id)
    VALUES
    ($user_id, $subject_id)
    RETURNING *;
  `
}

async function deleteUserSubject(userId, subjectId) {
  const query = `
    DELETE FROM users_subjects
    WHERE user_id = $user_id AND subject_id = $subject_id;
  `
}

module.exports = { listUserSubjects, insertUserSubject, deleteUserSubject }
