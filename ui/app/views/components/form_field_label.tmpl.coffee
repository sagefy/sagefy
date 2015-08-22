c = require('../../modules/content').get
requiredFn = require('../../modules/validations').required

module.exports = (data) ->
    return label(
        {for: data.name}
        data.label or ''
        span(
            {className: if isRequired then 'required' else 'optional'}
            if isRequired then c('required') else c('optional')
        ) unless data.type is 'message'
    )
