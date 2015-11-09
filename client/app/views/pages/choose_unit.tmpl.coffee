{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div({className: 'spinner'}) unless data.units
    return div(
        {id: 'choose-unit', className: 'col-10'}
        h1('Choose Unit')
    )
