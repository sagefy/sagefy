const Joi = require('joi')
const bcrypt = require('bcrypt')

const db = require('./index')
const { convertToUuid, generateSlug } = require('../helpers/uuidSlug')
const config = require('../config')

const SALT_ROUNDS = config.test ? 3 : 12

const userSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  name: Joi.string().min(1),
  email: Joi.string()
    .min(1)
    .email(),
  password: Joi.string()
    .min(8)
    .regex(/^\$2a\$.*$/),
  settings: Joi.object().keys({
    email_frequency: Joi.string().valid(
      'immediate',
      'daily',
      'weekly',
      'never'
    ),
    view_subjects: Joi.string().valid('public', 'private'),
    view_follows: Joi.string().valid('public', 'private'),
  }),
})

async function getUserById(userId) {
  const query = `
    SELECT *
    FROM users
    WHERE id = $1
    LIMIT 1;
  `
  const params = [convertToUuid(userId)]
  return db.getOne(query, params)
}

async function getUserByEmail(email) {
  const query = `
    SELECT *
    FROM users
    WHERE email = $1
    LIMIT 1;
  `
  const params = [email]
  return db.getOne(query, params)
}

async function getUserByName(name) {
  const query = `
    SELECT *
    FROM users
    WHERE name = $1
    LIMIT 1;
  `
  const params = [name]
  return db.getOne(query, params)
}

async function getUser({ id, email, name } = {}) {
  if (id) {
    return getUserById(id)
  }
  if (email) {
    return getUserByEmail(email)
  }
  if (name) {
    return getUserByName(name)
  }
  return null
}

async function listUsers() {
  const query = `
    SELECT *
    FROM users
    ORDER BY created DESC;
  `
  return db.list(query)
}

async function listUsersByUserIds(userIds) {
  const query = `
    SELECT *
    FROM users
    WHERE id in $1
    ORDER BY created DESC;
  `
  const params = [userIds.map(convertToUuid)]
  return db.list(query, params)
}

async function insertUser({ name, email, password: plainPassword }) {
  const query = `
    INSERT INTO users
    (name, email, password, settings)
    VALUES
    ($1,   $2,    $3,       $4)
    RETURNING *;
  `
  const password = await bcrypt.hash(plainPassword, SALT_ROUNDS)
  Joi.assert(
    { name, email, password },
    userSchema.requiredKeys('name', 'email', 'password')
  )
  const params = [
    name.toLowerCase().trim(),
    email.toLowerCase().trim(),
    password,
    {
      email_frequency: 'daily',
      view_subjects: 'private',
      view_follows: 'private',
    },
  ]
  const result = await db.getOne(query, params)
  // TODO update ES
  // TODO email user
  return result
}

async function updateUser({ id, name, email, settings }) {
  const query = `
    UPDATE users
    SET name = $2, email = $3, settings = $4
    WHERE id = $1
    RETURNING *;
  `
  Joi.assert(
    { id, name, email, settings },
    userSchema.requiredKeys('id', 'name', 'email', 'password')
  )
  const params = [
    convertToUuid(id),
    name.toLowerCase().trim(),
    email.toLowerCase().trim(),
    settings,
  ]
  const result = await db.getOne(query, params)
  // TODO update ES
  return result
}

async function updateUserPassword({ id, password: plainPassword }) {
  const query = `
    UPDATE users
    SET password = $2
    WHERE id = $1
    RETURNING *;
  `
  const password = await bcrypt.hash(plainPassword, SALT_ROUNDS)
  Joi.assert({ id, password }, userSchema.requiredKeys('id', 'password'))
  const params = [convertToUuid(id), password]
  const result = await db.getOne(query, params)
  // TODO update ES
  return result
}

async function anonymizeUser(id) {
  const query = `
    UPDATE users
    SET name = $2, email = $3, password = $4
    WHERE id = $id
    RETURNING *;
  `
  const name = generateSlug()
  const email = `${generateSlug()}@example.com`
  const password = await bcrypt.hash(generateSlug(), SALT_ROUNDS)
  const params = [convertToUuid(id), name, email, password]
  const result = await db.getOne(query, params)
  // TODO update ES
  return result
}

module.exports = {
  getUserById,
  getUserByEmail,
  getUserByName,
  getUser,
  listUsers,
  listUsersByUserIds,
  insertUser,
  updateUser,
  updateUserPassword,
  anonymizeUser,
}
