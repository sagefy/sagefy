Model = require('../framework/model')

class PostModel extends Model
    schema: {
        user_id: {
            type: 'hidden'
            validations: {}
        }
        topic_id: {
            type: 'hidden'
            validations: {}
        }
        body: {
            type: 'textarea'
            validations: {}
        }
        kind: {
            type: 'select'
            validations: {}
        }
        replies_to_id: {
            type: 'hidden'
            validations: {}
        }
        status: {  # Proposal/Flag only
            type: 'hidden'
            validations: {}
        }
        entity_version_id: {  # Proposal/Flag only
            type: 'hidden'
            validations: {}
        }
        name: {  # Proposal only
            type: 'text'
            validations: {}
        }
        action: {  # Proposal only
            type: 'select'
            validations: {}
        }
        response: {  # Vote only
            type: 'select'
            validations: {}
        }
        reason: {  # Flag only
            type: 'select'
            validations: {}
        }
    }

module.exports = PostModel
