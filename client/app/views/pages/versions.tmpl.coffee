{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div(
        {id: 'versions', className: 'col-10'}
        h1('Versions')
    )

    # TODO@ link back to entity
