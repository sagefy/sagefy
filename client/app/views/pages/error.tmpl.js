const {div, h1, p} = require('../../modules/tags')
const c = require('../../modules/content').get

module.exports = () =>
    div(
        {id: 'error', className: 'page'},
        [
            h1('404'),
            p(c('not_found'))
        ]
    )
