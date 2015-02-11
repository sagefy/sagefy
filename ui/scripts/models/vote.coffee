Model = require('../framework/model')

class VoteModel extends Model
    schema: {
        body: {
            type: 'textarea'
            validations: {}
        }
        replies_to_id: {
            type: 'select'
            validations: {}
        }
        response: {
            type: 'select'
            validations: {}
        }
    }

module.exports = VoteModel
