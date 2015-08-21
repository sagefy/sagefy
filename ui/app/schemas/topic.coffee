validations = require('../modules/validations')

module.exports = {
    name: {
        type: 'text'
        validations: [validations.required]
    }
    entity: {
        type: 'hidden'
        validations: [validations.required]
    }
}
