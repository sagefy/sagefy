{form} = require('../../modules/tags')
formField = require('./form_field.tmpl')

module.exports = (fields) ->
    return form(formField(field) for field in fields)
