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
        columns: ['tag']
    }
    require_ids: {
        type: 'list'
        validations: []
        columns: ['id']
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
