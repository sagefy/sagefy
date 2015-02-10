Model = require('../framework/model')

class PostModel extends Model
    schema: {
        user_id: {
            type: 'hidden'
        }
        topic_id: {
            type: 'hidden'
        }
        body: {
            type: 'textarea'
        }
        kind: {
            type: 'select'
        }
        replies_to_id: {
            type: 'hidden'
        }
        status: {  # Proposal/Flag only
            type: 'hidden'
        }
        entity_version_id: {  # Proposal/Flag only
            type: 'hidden'
        }
        name: {  # Proposal only
            type: 'text'
        }
        action: {  # Proposal only
            type: 'select'
        }
        response: {  # Vote only
            type: 'select'
        }
        reason: {  # Flag only
            type: 'select'
        }
    }

module.exports = PostModel
