const c = require('../../helpers/content').get
const { required } = require('../../helpers/validations')
const { label, span } = require('../../helpers/tags')

module.exports = data => {
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
