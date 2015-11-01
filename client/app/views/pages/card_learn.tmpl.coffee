{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div(
        {
            id: 'card-learn'
            className: 'col-10'
        }
    )
