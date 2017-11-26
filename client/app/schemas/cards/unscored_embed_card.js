const { required } = require('../../modules/validations')
const { extend } = require('../../modules/utilities')
const cardSchema = require('../card')

module.exports = extend({}, cardSchema, {
    'data.url': {
        type: 'text',
        validations: [required],
    },
})
