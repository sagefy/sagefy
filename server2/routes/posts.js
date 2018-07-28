const express = require('express')

const router = express.Router()

router.get('/', (req, res) => res.json({}))

router.post('/', (req, res) => res.json({}))

router.put('/:postId', (req, res) => res.json({}))

module.exports = router
