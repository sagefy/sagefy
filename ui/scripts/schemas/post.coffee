validations = require('../modules/validations')

module.exports = {
    user_id: {
        type: 'hidden'
        validations: []
    }
    topic_id: {
        type: 'hidden'
        validations: []
    }
    body: {
        type: 'textarea'
        validations: [
            validations.required
        ]
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
        validations: [
            validations.required
        ]
    }
    replies_to_id: {
        type: 'hidden'
        validations: []
    }
}
