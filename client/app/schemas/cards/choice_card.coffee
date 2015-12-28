{required} = require('../../modules/validations')
{extend} = require('../../modules/utilities')
cardSchema = require('../card')

module.exports = extend({}, cardSchema, {
    body: {
        type: 'textarea'
        validations: [required]
    }
    options: {
        type: 'list'
        validations: [required]
        columns: ['correct', 'value', 'feedback']
    }
    order: {
        type: 'select'
        validations: [required]
        options: [
            {value: 'random'}
            {value: 'set'}
        ]
        default: 'random'
    }
    max_options_to_show: {
        type: 'number'
        validations: [required]
        default: 4
    }
})
