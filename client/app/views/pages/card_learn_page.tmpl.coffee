{div} = require('../../modules/tags')
c = require('../../modules/content').get

# see: https://github.com/Matt-Esch/virtual-dom/issues/345

module.exports = (data) ->
    return div()
