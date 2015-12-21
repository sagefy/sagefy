post = require('./post')
{extend} = require('../modules/utilities')
{required} = require('../modules/validations')

module.exports = extend({}, post, {
    entity_version_id: {
        type: 'hidden'
        validations: []
    }
    name: {
        type: 'text'
        validations: [required]
    }
})
