const { h1, div } = require('../../modules/tags')
// const c = require('../../modules/content').get
const format = require('../../modules/format')

module.exports = data => {
  const { name } = data
  const { body } = data.data
  return div(h1(name), format(body, { highestHeading: 2 }))
}
