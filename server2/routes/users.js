const express = require('express')
const pick = require('lodash.pick')
const omit = require('lodash.omit')
const gravatar = require('gravatar')
const bcrypt = require('bcrypt')

const {
  getUserById,
  getUserByEmail,
  listUsersByUserIds,
  insertUser,
  updateUser,
  updateUserPassword,
  anonymizeUser,
} = require('../database/users')
const auth = require('../middleware/authMiddleware')
const abort = require('../helpers/abort')
const { generateSlug } = require('../helpers/uuidSlug')
const sendMail = require('../helpers/mail')
const config = require('../config')

const router = express.Router()

const SALT_ROUNDS = config.test ? 3 : 12

const WELCOME_TEXT = `
Welcome to Sagefy!

If you did not create this account, please reply immediately.

If you are interested in biweekly updates on Sagefy's progress,
sign up at https://sgef.cc/devupdates

Thank you!
`
const TOKEN_TEXT = `
To change your password, please visit {url}

If you did not request a password change, please reply immediately.
`
const PASSWORD_TEXT = `
You updated your Sagefy password.

If you did not change your password, please reply immediately.
`

router.get('/:userId', async (req, res) => {
  const { userId: id } = req.params
  const user = await getUserById(id)
  if (!user) throw abort(404, 'QqgmNTlCg0CGIarLNRSpLg')
  res.json({
    user:
      id === req.session.user
        ? omit(user, ['password'])
        : pick(user, ['id', 'created', 'name']),
    avatar: gravatar.url(user.email, { d: 'mm', s: '48' }),
  })
})

router.get('/', async (req, res) => {
  const { user_ids: userIds } = req.body
  const users = await listUsersByUserIds(userIds)
  if (!users) throw abort(404, '4IAna7RmGk2yKQrbtLfWXg')
  res.json({
    users: users.map(user => pick(user, ['id', 'created', 'name'])),
    avatars: users.map(user => gravatar.url(user.email, { d: 'mm', s: '48' })),
  })
})

router.post('/', async (req, res) => {
  const user = await insertUser(req.body)
  await sendMail({
    to: user.email,
    subject: 'Welcome to Sagefy',
    body: WELCOME_TEXT,
  })
  req.session.regenerate(() => {
    req.session.user = user.id
    res.json({ user: omit(user, ['password']) })
  })
})

router.post('/token', async (req, res) => {
  const user = await getUserByEmail(req.body.email)
  if (!user) throw abort(404, 'NpOTy8Ttuk2vQ4B5YpJKEA')
  const token = generateSlug()
  req.session.token = await bcrypt.hash(token, SALT_ROUNDS)
  await sendMail({
    to: user.email,
    subject: 'Sagefy Password Request',
    body: TOKEN_TEXT.replace(
      '{url}',
      `https://sagefy.org/password_reset?token=${token}`
    ),
  })
  res.json({ message: 'OK' }) // !!! Do not output token !!!
})

router.put('/:userId', auth, async (req, res) => {
  const { userId: id } = req.params
  if (req.session.user !== id) throw abort(403, 'XMS2QYQuVUOebLnLKFmk1Q')
  const prev = await getUserById(id)
  if (!prev) throw abort(404, '6AAZjJtqAkKFGp8YkzJChQ')
  const user = await updateUser({ ...prev, ...req.body, id })
  res.json({ user: omit(user, ['password']) })
})

router.put('/:userId/password', async (req, res) => {
  const validToken = await bcrypt.compare(req.session.token, req.body.token)
  if (!validToken) throw abort(401, 'RVAgSR2bo06fPKTGO2AcVg')
  const { userId: id } = req.params
  const { password } = req.body
  const user = await updateUserPassword({ id, password })
  await sendMail({
    to: user.email,
    subject: 'Sagefy Password Reset',
    body: PASSWORD_TEXT,
  })
  res.json({ user: omit(user, ['password']) })
})

router.delete('/:userId', async (req, res) => {
  const validToken = await bcrypt.compare(req.session.token, req.body.token)
  if (!validToken) throw abort(401, 'm0BEbqfntUmuU4z3hkeO9A')
  const { userId: id } = req.params
  if (req.session.user !== id) throw abort(403, 'fmXJKKVWKUaB4rJSQVjkZw')
  const user = await anonymizeUser(id)
  res.json({ user: omit(user, ['password']) })
})

module.exports = router
