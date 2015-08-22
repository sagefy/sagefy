post = require('./post')
{extend} = require('../modules/utilities')

module.exports = extend({}, post, {
    body: {
        type: 'textarea'
        validations: []
    }
    replies_to_id: {
        type: 'hidden'
        validations: []
    }
    response: {
        type: 'select'
        validations: []
    }
})
