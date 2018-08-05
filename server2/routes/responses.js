const express = require('express')
const auth = require('../middleware/authMiddleware')
// const abort = require('../helpers/abort')

const router = express.Router()

router.post('/', auth, (req, res) => res.json({}))

module.exports = router
