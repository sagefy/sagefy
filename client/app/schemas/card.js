const {required} = require('../modules/validations')

module.exports = {
    language: {
        type: 'select',
        validations: [required],
        options: [
            {value: 'en'}
        ]
    },
    unit_id: {
        type: 'text',
        validations: [required]
    },
    name: {
        type: 'text',
        validations: [required]
    },
    tags: {
        type: 'list',
        validations: [],
        columns: [
            {name: 'tag', type: 'text'}
        ]
    },
    require_ids: {
        type: 'list',
        validations: [],
        columns: [
            {name: 'id', type: 'text'}
        ]
    },
    kind: {
        type: 'select',
        validations: [required],
        options: [
            {value: 'video'},
            {value: 'choice'}
        ]
    }
}
