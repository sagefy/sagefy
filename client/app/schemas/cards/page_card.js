const { required } = require('../../modules/validations')
const { extend } = require('../../modules/utilities')
const cardSchema = require('../card')

module.exports = extend({}, cardSchema, {
    'data.body': {
        type: 'textarea',
        validations: [required],
    },
})
