Model = require('../framework/model')

class FollowModel extends Model
    schema: {
        user_id: {
            type: 'hidden'
            validations: {}
        }
        entity: {
            type: 'hidden'
            validations: {}
        }
    }

module.exports = FollowModel
