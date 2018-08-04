const Joi = require('joi')

const db = require('./index')

const userSubjectSchema = Joi.object().keys({
  id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  userId: Joi.string()
    .guid()
    .required(),
  subjectId: Joi.string()
    .guid()
    .required(),
})

async function listUserSubjects(userId) {}

async function insertUserSubject(userId, subjectId) {}

async function deleteUserSubject(userId, subjectId) {}

module.exports = { listUserSubjects, insertUserSubject, deleteUserSubject }
