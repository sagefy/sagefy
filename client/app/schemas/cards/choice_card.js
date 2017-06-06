const { required } = require('../../modules/validations')
const { extend } = require('../../modules/utilities')
const cardSchema = require('../card')

module.exports = extend({}, cardSchema, {
    body: {
        type: 'textarea',
        validations: [required]
    },
    options: {
        type: 'list',
        validations: [required],
        columns: [
            {
                name: 'correct',
                type: 'select',
                options: [
                    { value: 'true' },
                    { value: 'false' }
                ]
            },
            { name: 'value', type: 'text' },
            { name: 'feedback', type: 'text' }
        ]
    },
    order: {
        type: 'select',
        validations: [required],
        options: [
            { value: 'random' },
            { value: 'set' }
        ],
        default: 'random'
    },
    max_options_to_show: {
        type: 'number',
        validations: [required],
        default: 4
    }
})
