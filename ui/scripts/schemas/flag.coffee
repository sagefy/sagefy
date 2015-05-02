post = require('./post')
util = require('../framework/utilities')

module.exports = util.extend({}, post, {
    status: {
        type: 'hidden'
        validations: []
    }
    entity_version_id: {
        type: 'hidden'
        validations: []
    }
    reason: {
        type: 'select'
        validations: []
    }
})
