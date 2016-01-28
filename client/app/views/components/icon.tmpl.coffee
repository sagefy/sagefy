{i} = require('../../modules/tags')

module.exports = (name) ->
    return i({className: "icon icon-#{name}"})
