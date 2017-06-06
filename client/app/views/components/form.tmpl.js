const { form } = require('../../modules/tags')
const formField = require('./form_field.tmpl')

module.exports = fields =>
    form(fields.map(field => formField(field)))
