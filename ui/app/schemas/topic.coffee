{required} = require('../modules/validations')

module.exports = {
    name: {
        type: 'text'
        validations: [required]
    }
    entity: {
        type: 'hidden'
        validations: [required]
    }
}
