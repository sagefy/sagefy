const { i } = require('../../modules/tags')

module.exports = name =>
    i({ className: `icon icon-${name}` })
