const Joi = require('joi')

const db = require('./index')

const userSubjectSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  userId: Joi.string().guid(),
  subjectId: Joi.string().guid(),
})

async function listUserSubjects(userId) {}

async function insertUserSubject(userId, subjectId) {}

async function deleteUserSubject(userId, subjectId) {}

module.exports = { listUserSubjects, insertUserSubject, deleteUserSubject }
