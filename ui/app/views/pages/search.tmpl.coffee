{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

# TODO When search for entity's topic, show create topic button

module.exports = (data) ->
    return div(
        {id: 'search', className: 'col-10'}
        h1('Search')
        div({className: 'spinner'})
    )
