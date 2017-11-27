const { a } = require('../../modules/tags')
const icon = require('./icon.tmpl')

module.exports = () =>
  a(
    {
      href: 'https://sagefy.uservoice.com/forums/233394-general',
      className: 'feedback',
    },
    icon('contact'),
    ' Feedback'
  )
