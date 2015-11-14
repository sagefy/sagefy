{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div({className: 'spinner'}) unless data.card

    return div(
        {id: 'card', className: 'col-10'}
        h1('Card')
    )

    # TODO@ show create topic button
