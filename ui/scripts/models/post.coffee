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
            validations: {
                required: true
            }
        }
        kind: {
            type: 'select'
            options: [
                {label: 'Post', value: 'post'}
                {label: 'Proposal', value: 'proposal'}
                {label: 'Vote', value: 'vote'}
                {label: 'Flag', value: 'flag'}
            ]
            validations: {
                required: true
            }
        }
        replies_to_id: {
            type: 'hidden'
            validations: {}
        }
    }

module.exports = PostModel
