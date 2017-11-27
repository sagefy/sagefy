const { button } = require('../../modules/tags')
const icon = require('./icon.tmpl')

module.exports = (data) => {
  return button(
    {
      type: 'submit',
      disabled: data.disabled,
      id: data.id,
    },
    icon(data.icon),
    ' ',
    data.label
  )
}
