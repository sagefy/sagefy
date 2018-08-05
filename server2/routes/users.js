const express = require('express')
const pick = require('lodash.pick')
const omit = require('lodash.omit')
const gravatar = require('gravatar')

const {
  getUserById,
  listUsersByUserIds,
  insertUser,
  updateUser,
  updateUserPassword,
  anonymizeUser,
} = require('../database/users')
const auth = require('../middleware/authMiddleware')
const abort = require('../helpers/abort')

const router = express.Router()

router.get('/:userId', async (req, res) => {
  const { userId: id } = req.params
  const user = await getUserById(id)
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
  let users = await listUsersByUserIds(userIds)
  users = users.map(user => pick(user, ['id', 'created', 'name']))
  res.json({
    users,
    avatars: users.map(user => gravatar.url(user.email, { d: 'mm', s: '48' })),
  })
})

// TODO move these to the entity routes?
router.get('/:userId/units--created', (req, res) => res.json({}))

router.get('/:userId/cards--created', (req, res) => res.json({}))

router.get('/:userId/subjects--created', (req, res) => res.json({}))

router.post('/', async (req, res) => {
  const user = await insertUser(req.body)
  req.session.regenerate(() => {
    req.session.user = user.id
    res.json({ user: omit(user, ['password']) })
  })
})

router.post('/token', (req, res) => res.json({})) // Do not output token

// TODO create responses route?
router.post('/:userId/responses', auth, (req, res) => res.json({}))

router.put('/:userId', auth, async (req, res) => {
  const { userId: id } = req.params
  if (req.session.user !== id) throw abort(403, 'XMS2QYQuVUOebLnLKFmk1Q')
  const prev = await getUserById(id)
  const user = await updateUser({ ...prev, ...req.body, id })
  res.json({ user: omit(user, ['password']) })
})

router.put('/:userId/password', auth, async (req, res) => {
  const { userId: id } = req.params
  const { password } = req.body
  // TODO validate token, remove auth
  const user = await updateUserPassword({ id, password })
  res.json({ user: omit(user, ['password']) })
})

router.delete('/:userId', auth, async (req, res) => {
  const { userId: id } = req.params
  if (req.session.user !== id) throw abort(403, 'fmXJKKVWKUaB4rJSQVjkZw')
  // TODO validate token, remove auth
  const user = await anonymizeUser(id)
  res.json({ user: omit(user, ['password']) })
})

module.exports = router
