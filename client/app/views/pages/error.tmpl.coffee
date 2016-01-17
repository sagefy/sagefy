{div, h1, p} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div(
        {id: 'error'}
        [
            h1('404')
            p(c('not_found'))
        ]
    )
