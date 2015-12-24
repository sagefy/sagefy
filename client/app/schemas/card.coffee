{required} = require('../modules/validations')

module.exports = {
    language: {
        type: 'select'
        validations: [required]
        options: [
            {value: 'en'}
        ]
    }
    unit_id: {
        type: 'select'
        validations: [required]
    }
    name: {
        type: 'text'
        validations: [required]
    }
    tags: {
        type: 'list'
        validations: []
    }
    require_ids: {
        type: 'list'
        validations: []
    }
    kind: {
        type: 'select'
        validations: [required]
        options: [
            {value: 'video'}
            {value: 'choice'}
        ]
    }
}
