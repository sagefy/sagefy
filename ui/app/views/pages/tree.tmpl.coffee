{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div(
        {id: 'tree', className: 'col-10'}
        h1('Set Tree')
    )
