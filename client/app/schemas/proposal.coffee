post = require('./post')
{extend} = require('../modules/utilities')

module.exports = extend({}, post, {
    status: {
        type: 'hidden'
        validations: []
    }
    entity_version_id: {
        type: 'hidden'
        validations: []
    }
    name: {
        type: 'text'
        validations: []
    }
    action: {
        type: 'select'
        validations: []
    }
})
