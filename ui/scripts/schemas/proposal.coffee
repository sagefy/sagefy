post = require('./post')
util = require('../framework/utilities')

module.exports = util.extend({}, post, {
    status: {
        type: 'hidden'
        validations: {}
    }
    entity_version_id: {
        type: 'hidden'
        validations: {}
    }
    name: {
        type: 'text'
        validations: {}
    }
    action: {
        type: 'select'
        validations: {}
    }
})
