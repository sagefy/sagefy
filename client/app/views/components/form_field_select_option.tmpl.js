const { li, label, input } = require('../../modules/tags')

module.exports = data =>
  li(
    label(
      {
        className: `form-field--select__label${data.disabled
          ? ' form-field--select__label--disabled'
          : ''}`,
      },
      input({
        type: data.multiple ? 'checkbox' : 'radio',
        value: data.value || '',
        name: data.name,
        checked: data.checked,
        disabled: data.disabled || false,
      }),
      ' ',
      data.label
    )
  )
