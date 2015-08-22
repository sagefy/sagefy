{div, h1, p} = require('../../modules/tags')

module.exports = (data) ->
    return div(
        h1(
            data.title
        ) if data.title
        p(
            data.description
        ) if data.description
        div(
            {className: 'form'}
        )
    )
