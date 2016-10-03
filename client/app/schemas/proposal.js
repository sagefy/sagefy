const post = require('./post')
const {extend} = require('../modules/utilities')
const {required} = require('../modules/validations')

module.exports = extend({}, post, {
    name: {
        type: 'text',
        validations: [required]
    },
    'entity_version.id': {
        type: 'hidden',
        validations: []
    },
    'entity_version.kind': {
        type: 'select',
        options: [
            {value: 'card'},
            {value: 'unit'},
            {value: 'set'}
        ],
        validations: [required]
    }
})
