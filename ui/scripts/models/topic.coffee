Model = require('../framework/model')

class TopicModel extends Model
    schema: {
        name: {
            type: 'text'
            validations: {
                required: true
            }
        }
        entity: {
            type: 'hidden'
            validations: {
                required: true
            }
        }
    }

module.exports = TopicModel
