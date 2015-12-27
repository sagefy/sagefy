{required} = require('../modules/validations')

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
            required
        ]
    }
    kind: {
        type: 'select'
        options: [
            {value: 'post'}
            {value: 'proposal'}
            {value: 'vote'}
            {value: 'flag'}
        ]
        default: 'post'
        validations: [
            required
        ]
    }
    replies_to_id: {
        type: 'hidden'
        validations: []
    }
}
