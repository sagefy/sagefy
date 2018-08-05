const elasticsearch = require('elasticsearch')

const config = require('../config')

module.exports = new elasticsearch.Client(config.es)
