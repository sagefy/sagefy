{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div({className: 'spinner'}) unless data.set

    return div(
        {id: 'set', className: 'col-10'}
        h1('Set')
    )
