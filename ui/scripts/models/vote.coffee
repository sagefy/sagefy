PostModel = require('./post')
util = require('../framework/utilities')

class VoteModel extends PostModel
    schema: util.extend({}, PostModel::schema, {
        body: {
            type: 'textarea'
            validations: {}
        }
        replies_to_id: {
            type: 'hidden'
            validations: {}
        }
        response: {
            type: 'select'
            validations: {}
        }
    })

module.exports = VoteModel
