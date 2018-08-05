const express = require('express')
const pick = require('lodash.pick')
const bcrypt = require('bcrypt')

const abort = require('../helpers/abort')
const auth = require('../middleware/authMiddleware')
const { getUser } = require('../database/users')
const { convertToSlug } = require('../helpers/uuidSlug')

const router = express.Router()

const VISIBILE_FIELDS = ['user', 'subject', 'unit', 'card']

// Get the current userId and next
router.get('/', auth, (req, res) => {
  res.json(pick(req.session, VISIBILE_FIELDS))
})

// Log in: create a new session
router.post('/', async (req, res) => {
  const user = await getUser(req.body)
  if (!user) throw abort(404, 'yEcszBaVVEmfKEiCX7oJkQ')
  const match = await bcrypt.compare(req.body.password, user.password)
  if (!match) throw abort(401, 'Badi1ATnBUCVDkI8jGiiwA')
  req.session.regenerate(() => {
    req.session.user = convertToSlug(user.id)
    res.json(pick(req.session, VISIBILE_FIELDS))
  })
})

// Choose a subject or unit
router.put('/', auth, (req, res) => {
  const { subject, unit } = req.body
  if (subject) req.session.subject = subject
  if (unit) req.session.unit = unit
  res.json(pick(req.session, VISIBILE_FIELDS))
})

// Log out: delete the session
router.delete('/', (req, res, next) => {
  req.session.destroy(next)
})

module.exports = router
