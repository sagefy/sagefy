PostModel = require('./post')
util = require('../framework/utilities')

class FlagModel extends PostModel
    schema: util.extend({}, PostModel::schema, {
        status: {
            type: 'hidden'
            validations: {}
        }
        entity_version_id: {
            type: 'hidden'
            validations: {}
        }
        reason: {
            type: 'select'
            validations: {}
        }
    })

module.exports = FlagModel
