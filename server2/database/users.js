const Joi = require('joi')

const db = require('./index')

const userSchema = Joi.object().keys({
  id: Joi.string()
    .guid()
    .required(),
  created: Joi.date().required(),
  modified: Joi.date().required(),
  name: Joi.string()
    .min(1)
    .required(),
  email: Joi.string()
    .min(1)
    .email()
    .required(),
  password: Joi.string()
    .min(8)
    .regex(/^\$2a\$.*$/)
    .required(),
  settings: Joi.object()
    .keys({
      email_frequency: Joi.string()
        .valid('immediate', 'daily', 'weekly', 'never')
        .required(),
      view_subjects: Joi.string()
        .valid('public', 'private')
        .required(),
      view_follows: Joi.string()
        .valid('public', 'private')
        .required(),
    })
    .required(),
})

async function getUser(params) {}

async function getUserById(userId) {}

async function getUserByEmail(email) {}

async function getUserByName(name) {}

async function listUsers() {}

async function listUsersByUserIds(userIds) {}

async function insertUser(data) {}

async function updateUser(prev, data) {}

async function updateUserPassword(prev, data) {}

async function deleteUser(userId) {}

module.exports = {
  getUser,
  getUserById,
  getUserByEmail,
  getUserByName,
  listUsers,
  listUsersByUserIds,
  insertUser,
  updateUser,
  updateUserPassword,
  deleteUser,
}
