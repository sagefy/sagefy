{required} = require('../modules/validations')

module.exports = {
    language: {
        type: 'select'
        validations: [required]
        options: [
            {value: 'en'}
        ]
    }
    name: {
        type: 'text'
        validations: [required]
    }
    body: {
        type: 'textarea'
        validations: [required]
    }
    tags: {
        type: 'list'
        validations: []
        columns: [
            {name: 'tag', type: 'text'}
        ]
    }
    require_ids: {
        type: 'list'
        validations: []
        columns: [
            {name: 'id', type: 'text'}
        ]
    }
}
