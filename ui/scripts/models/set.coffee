Model = require('../framework/model')

class SetModel extends Model
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
        members: {
            type: 'select'
            validations: {}
        }
    }

module.exports = SetModel
