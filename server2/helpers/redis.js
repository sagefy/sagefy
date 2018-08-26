const redis = require('redis')
const { promisify } = require('util')
const { fromPairs } = require('lodash')
const config = require('../config')

const client = redis.createClient(config.redis)

module.exports = fromPairs(
  ['get', 'set', 'setex', 'ttl', 'del'].map(k => [
    k,
    promisify(client[k]).bind(client),
  ])
)
