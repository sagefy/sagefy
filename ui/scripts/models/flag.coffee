Model = require('../framework/model')

class FlagModel extends Model
    schema: {
        reason: {
            type: 'select'
            validations: {}
        }
        body: {
            type: 'textarea'
            validations: {}
        }
        topic_id: {
            type: 'hidden'
            validations: {}
        }
    }

module.exports = FlagModel
