post = require('./post')
{extend} = require('../modules/utilities')
{required} = require('../modules/validations')

module.exports = extend({}, post, {
    name: {
        type: 'text'
        validations: [required]
    }
    'entity.id': {
        type: 'text'
        validations: [required]
    }
    'entity.kind': {
        type: 'text'
        validations: [required]
    }
})
