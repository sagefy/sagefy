const post = require('./post')
const { extend } = require('../modules/utilities')
const { required } = require('../modules/validations')

module.exports = extend({}, post, {
    'entity_version.id': {
        type: 'hidden',
        validations: [],
    },
    'entity_version.kind': {
        type: 'select',
        options: [
            { value: 'card' },
            { value: 'unit' },
            { value: 'subject' },
        ],
        validations: [required],
    },
})
