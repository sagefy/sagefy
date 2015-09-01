c = require('../../modules/content').get
{required} = require('../../modules/validations')
{label, span} = require('../../modules/tags')

module.exports = (data) ->
    isRequired = if data.validations \
                 then required in data.validations \
                 else false
    return label(
        {for: data.name}
        data.label or ''
        span(
            {className: if isRequired then 'required' else 'optional'}
            if isRequired then c('required') else c('optional')
        ) unless data.type is 'message'
    )
