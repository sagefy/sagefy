Model = require('../framework/model')

class CardModel extends Model
    schema: {
        language: {
            type: 'select'
            validations: {}
        }
        unit_id: {
            type: 'select'
            validations: {}
        }
        name: {
            type: 'text'
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
        kind: {
            type: 'select'
            validations: {}
        }
    }

module.exports = CardModel
