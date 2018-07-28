const express = require('express')

const router = express.Router()

router.get('/', (req, res) => res.json({}))

router.post('/:subjectId', (req, res) => res.json({}))

router.delete('/:subjectId', (req, res) => res.json({}))

module.exports = router
