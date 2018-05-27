const { h1, div } = require('../../helpers/tags')
// const c = require('../../helpers/content').get
const format = require('../../helpers/format')

module.exports = data => {
  const { name } = data
  const { body } = data.data
  return div(h1(name), format(body, { highestHeading: 2 }))
}
