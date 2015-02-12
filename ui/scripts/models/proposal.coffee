PostModel = require('./post')
util = require('../framework/utilities')

class ProposalModel extends PostModel
    schema: util.extend({}, PostModel::schema, {
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

module.exports = ProposalModel
