// TODO-3 move copy to content directory
const { div, h1 } = require('../../modules/tags')
const terms = require('./terms.content')

module.exports = () =>
  div(
    { id: 'terms', className: 'page' },
    h1('Sagefy Privacy Policy & Terms of Service'),
    terms
  )
