{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div(
        {id: 'search', className: 'col-10'}
        h1('Search')
        div({className: 'spinner'})
    )
