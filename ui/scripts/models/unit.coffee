Model = require('../framework/model')

class UnitModel extends Model
    schema: {
        language: {
            type: 'select'
            validations: {}
        }
        name: {
            type: 'text'
            validations: {}
        }
        body: {
            type: 'textarea'
            validations: {}
        }
        tags: {
            type: 'select'
            validations: {}
        }
        require_ids: {
            type: 'select'
            validations: {}
        }
    }

module.exports = UnitModel
