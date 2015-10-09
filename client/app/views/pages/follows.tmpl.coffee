{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div(
        {id: 'follows', className: 'col-10'}
        h1('Follows')
    )

    # TODO link back notices
