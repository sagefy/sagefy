const Joi = require('joi')
const bcrypt = require('bcryptjs')
const { pick } = require('lodash')
const gravatar = require('gravatar')

const db = require('./index')
const { generateSlug } = require('../helpers/uuidSlug')
const config = require('../config')
const es = require('../helpers/es')

const SALT_ROUNDS = config.test ? 3 : 12

const userSchema = Joi.object().keys({
  id: Joi.string().guid(),
  created: Joi.date(),
  modified: Joi.date(),
  name: Joi.string().min(1),
  email: Joi.string().email(),
  password: Joi.string().regex(/^\$2a\$.*$/),
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

const plainPasswordSchema = Joi.string()
  .min(8)
  .required()

async function sendUserToEs(user) {
  return es.index({
    index: 'entity',
    type: 'user',
    body: {
      ...pick(user, ['id', 'created', 'name']),
      avatar: gravatar.url(user.email, { d: 'mm', s: '48' }),
    },
    id: user.id,
  })
}

async function getUserById(userId) {
  const query = `
    SELECT *
    FROM users
    WHERE id = $id
    LIMIT 1;
  `
  return db.get(query, { userId })
}

async function getUserByEmail(email) {
  const query = `
    SELECT *
    FROM users
    WHERE email = $email
    LIMIT 1;
  `
  return db.get(query, { email })
}

async function getUserByName(name) {
  const query = `
    SELECT *
    FROM users
    WHERE name = $name
    LIMIT 1;
  `
  return db.get(query, { name })
}

async function getUser({ id, email, name } = {}) {
  if (id) return getUserById(id)
  if (email) return getUserByEmail(email)
  if (name) return getUserByName(name)
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

async function listUsersByUserIds(ids) {
  const query = `
    SELECT *
    FROM users
    WHERE id in $ids
    ORDER BY created DESC;
  `
  return db.list(query, { ids })
}

async function insertUser({ name, email, password: plainPassword }) {
  Joi.assert(plainPassword, plainPasswordSchema)
  const params = {
    name: name.toLowerCase().trim(),
    email: email.toLowerCase().trim(),
    password: await bcrypt.hash(plainPassword, SALT_ROUNDS),
    settings: {
      email_frequency: 'daily',
      view_subjects: 'private',
      view_follows: 'private',
    },
  }
  Joi.assert(params, userSchema.requiredKeys(Object.keys(params)))
  const query = `
    INSERT INTO users
    ( name,  email,  password,  settings)
    VALUES
    ($name, $email, $password, $settings)
    RETURNING *;
  `
  const user = await db.save(query, params)
  await sendUserToEs(user)
  return user
}

async function updateUser({ id, name, email, settings }) {
  const params = {
    id,
    name: name.toLowerCase().trim(),
    email: email.toLowerCase().trim(),
    settings,
  }
  Joi.assert(params, userSchema.requiredKeys(Object.keys(params)))
  const query = `
    UPDATE users
    SET name = $name, email = $email, settings = $settings
    WHERE id = $id
    RETURNING *;
  `
  const user = await db.save(query, params)
  await sendUserToEs(user)
  return user
}

async function updateUserPassword({ id, password: plainPassword }) {
  Joi.assert(plainPassword, plainPasswordSchema)
  const params = {
    id,
    password: await bcrypt.hash(plainPassword, SALT_ROUNDS),
  }
  Joi.assert(params, userSchema.requiredKeys(Object.keys(params)))
  const query = `
    UPDATE users
    SET password = $password
    WHERE id = $id
    RETURNING *;
  `
  const user = await db.save(query, params)
  return user
}

async function anonymizeUser(id) {
  const query = `
    UPDATE users
    SET name = $name, email = $email, password = $password
    WHERE id = $id
    RETURNING *;
  `
  const name = generateSlug()
  const email = `${generateSlug()}@example.com`
  const password = await bcrypt.hash(generateSlug(), SALT_ROUNDS)
  const user = await db.save(query, { id, name, email, password })
  await sendUserToEs(user)
  return user
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
