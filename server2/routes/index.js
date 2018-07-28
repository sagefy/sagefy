const express = require('express')

const router = express.Router()

router.get('/', (req, res) =>
  res.json({ message: 'Welcome to the Sagefy service!' })
)

router.get('/sitemap', (req, res) => res.json({}))

router.get('/search', (req, res) => res.json({}))

module.exports = router
