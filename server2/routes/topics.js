const express = require('express')

const router = express.Router()

router.get('/:topicId', (req, res) => res.json({}))

router.get('/', (req, res) => res.json({}))

router.post('/', (req, res) => res.json({}))

router.put('/:topicId', (req, res) => res.json({}))

module.exports = router
