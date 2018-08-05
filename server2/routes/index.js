const express = require('express')

const es = require('../helpers/es')

const router = express.Router()

router.get('/', (req, res) => {
  res.json({ message: 'Welcome to the Sagefy service!' })
})

router.get('/sitemap', (req, res) => res.json({}))

router.get('/search', async (req, res) => {
  // elasticsearch doc: http://bit.ly/1NdvIoi
  const result = await es.search({
    index: 'entity',
    type: req.params.kind || 'user,card,unit,subject,topic,post',
    q: req.params.q,
    size: req.params.limit || 10,
    from: req.params.offset || 0,
  })
  res.json(result.hits)
})

module.exports = router
