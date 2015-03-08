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
                {label: 'Post', value: 'post'}  # TODO@ label is a view concern
                {label: 'Proposal', value: 'proposal'}
                {label: 'Vote', value: 'vote'}
                {label: 'Flag', value: 'flag'}
            ]
            default: 'post'
            validations: {
                required: true
            }
        }
        replies_to_id: {
            type: 'hidden'
            validations: {}
        }
    }

    constructor: (attributes) ->
        if attributes and attributes.kind in ['proposal', 'vote', 'flag']
            return
        super

module.exports = PostModel
