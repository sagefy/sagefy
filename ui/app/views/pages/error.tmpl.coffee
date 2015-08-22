{div, h1, p} = require('../../modules/tags')

module.exports = (data) ->
    return div(
        {id: 'error', className: 'col-4'}
        h1(
            data.code
            p(
                data.message
            ) if data.message
        )
    )
