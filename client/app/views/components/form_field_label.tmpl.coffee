c = require('../../modules/content').get
{required} = require('../../modules/validations')
{label, span} = require('../../modules/tags')

module.exports = (data) ->
    isRequired = if data.validations \
                 then required in data.validations \
                 else false
    return label(
        {
            className: 'form-field__label'
            for: "ff-#{data.name}"
        }
        data.label or ''
        span(
            {
                className: (
                    if isRequired \
                        then 'form-field__required'
                        else 'form-field__optional'
                )
            }
            if isRequired then c('required') else c('optional')
        ) unless data.type is 'message'
    )
