const c = require('../../modules/content').get
const { required } = require('../../modules/validations')
const { label, span } = require('../../modules/tags')

module.exports = (data) => {
    const isRequired = data.validations
        ? data.validations.indexOf(required) > -1
        : false
    return label(
        {
            className: 'form-field__label',
            for: `ff-${data.name}`,
        },
        data.label || '',
        data.type === 'message'
            ? null
            : span(
                {
                    className: isRequired
                          ? 'form-field__required'
                          : 'form-field__optional',
                },
                  isRequired ? c('required') : c('optional')
              )
    )
}
