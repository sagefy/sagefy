{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div(
        {id: 'my-sets', className: 'col-10'}
        h1('My Sets')
        div({className: 'spinner'})
    )
