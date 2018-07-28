const express = require('express')

const router = express.Router()

router.get('/', (req, res) => res.json({}))

router.put('/:noticeId', (req, res) => res.json({}))

module.exports = router
