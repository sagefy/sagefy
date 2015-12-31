{required} = require('../modules/validations')

module.exports = {
    id: {
        type: 'hidden'
        validations: []
    }
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
