post = require('./post')
{extend} = require('../modules/utilities')
{required} = require('../modules/validations')

noop = ->

module.exports = extend({}, post, {
    body: {
        type: 'textarea'
        validations: [noop]
    }
    replies_to_id: {
        type: 'hidden'
        validations: [required]
    }
    response: {
        type: 'select'
        validations: [required]
        options: [
            {value: 'true'}
            {value: 'false'}
        ]
    }
})
