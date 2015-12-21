{required} = require('../modules/validations')

module.exports = {
    name: {
        type: 'text'
        validations: [required]
    }
    'entity.id': {
        type: 'hidden'
        validations: [required]
    }
    'entity.kind': {
        type: 'hidden'
        validations: [required]
    }
}
