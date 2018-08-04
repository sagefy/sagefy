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

/*

CREATE TABLE users_subjects (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id uuid NOT NULL REFERENCES users (id),
  subject_id uuid NOT NULL REFERENCES subjects_entity_id (entity_id),
  UNIQUE (user_id, subject_id)
);

schema = extend({}, default, {
  'tablename': 'users_subjects',
  'fields': {
    'user_id': {
      'validate': (is_required, is_uuid,),
    },
    'subject_id': {
      'validate': (is_required, is_uuid,),
    },
  },
})

*/

async function listUserSubjects(userId) {}

async function insertUserSubject(userId, subjectId) {}

async function deleteUserSubject(userId, subjectId) {}

module.exports = { listUserSubjects, insertUserSubject, deleteUserSubject }
