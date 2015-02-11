Model = require('../framework/model')

class ProposalModel extends Model
    schema: {
        topic_id: {
            type: 'hidden'
            validations: {}
        }
        body: {
            type: 'textarea'
            validations: {}
        }
        replies_to_id: {
            type: 'select'
            validations: {}
        }
        name: {
            type: 'text'
            validations: {}
        }
        action: {
            type: 'select'
            validations: {}
        }
    }

module.exports = ProposalModel
