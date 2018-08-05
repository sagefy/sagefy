const redis = require('redis')
const { promisify } = require('util')
const zipObject = require('lodash.zipobject')
const config = require('../config')

const client = redis.createClient(config.redis)

module.exports = zipObject(
  ['get', 'set', 'setex', 'delete'].map(k => promisify(client[k]).bind(client))
)
