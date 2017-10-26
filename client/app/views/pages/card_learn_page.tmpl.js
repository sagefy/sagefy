const { h1, div } = require('../../modules/tags')
// const c = require('../../modules/content').get
const format = require('../../modules/format')
// see: https://github.com/Matt-Esch/virtual-dom/issues/345

module.exports = (data) => {
    const { name } = data
    const { body } = data.data
    return div(
        h1(name),
        format(body, { highestHeading: 2 })
    )
}
