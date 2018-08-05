const express = require('express')

const router = express.Router()

router.get('/:cardId', (req, res) => res.json({}))

router.get('/versions/:versionId', (req, res) => res.json({}))

router.get('/', (req, res) => res.json({}))
// TODO option to get created by userId

router.get('/:cardId/versions', (req, res) => res.json({}))

router.post('/versions', (req, res) => res.json({}))

router.post('/:cardId/versions', (req, res) => res.json({}))

module.exports = router
