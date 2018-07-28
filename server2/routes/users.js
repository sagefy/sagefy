const express = require('express')

const router = express.Router()

router.get('/', (req, res) => res.json({}))

router.get('/:userId', (req, res) => res.json({}))

router.get('/:userId/units~created', (req, res) => res.json({}))

router.get('/:userId/cards~created', (req, res) => res.json({}))

router.get('/:userId/subjects~created', (req, res) => res.json({}))

router.post('/', (req, res) => res.json({}))

router.post('/token', (req, res) => res.json({}))

router.post('/:userId/responses', (req, res) => res.json({}))

router.put('/:userId/password', (req, res) => res.json({}))

router.put('/:userId', (req, res) => res.json({}))

router.delete('/:userId', (req, res) => res.json({}))

module.exports = router
