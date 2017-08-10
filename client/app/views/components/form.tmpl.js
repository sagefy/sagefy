const { form, ul } = require('../../modules/tags')
const formField = require('./form_field.tmpl')
const formError = require('./form_error.tmpl')

module.exports = ({ fields, errors }) =>
    form(
        fields.map(field => formField(field)),
        errors && errors.length
            ? ul(
                  { className: 'form__errors' },
                  errors.map(error => formError(error))
              )
            : null
    )
