post = require('./post')
{extend} = require('../modules/utilities')
{required} = require('../modules/validations')

module.exports = extend({}, post, {
    name: {
        type: 'text'
        validations: [required]
    }
    'entity.id': {
        type: 'hidden'
        validations: []
    }
    'entity.kind': {
        type: 'select'
        options: [
            {value: 'card'}
            {value: 'unit'}
            {value: 'set'}
        ]
        validations: [required]
    }
})
