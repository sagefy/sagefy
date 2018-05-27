const { li } = require('../../helpers/tags')
const icon = require('./icon.tmpl')

module.exports = ({ name, message }) =>
  li(
    { className: 'form__error' },
    icon('bad'),
    [' ', name ? `${name}: ` : '', message].join('')
  )
