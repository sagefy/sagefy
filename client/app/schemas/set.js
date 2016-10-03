const {required} = require('../modules/validations')

module.exports = {
    language: {
        type: 'select',
        validations: [required],
        options: [
            {value: 'en'}
        ]
    },
    name: {
        type: 'text',
        validations: [required]
    },
    body: {
        type: 'textarea',
        validations: [required]
    },
    tags: {
        type: 'list',
        validations: [],
        columns: [
            {name: 'tag', type: 'text'}
        ]
    },
    members: {
        type: 'list',
        validations: [required],
        columns: [
            {name: 'kind', type: 'select', options: [
                {value: 'unit'},
                {value: 'set'}
            ]},
            {name: 'id', type: 'text'}
        ]
    }
}
