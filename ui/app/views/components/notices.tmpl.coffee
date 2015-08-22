{ul} = require('../../modules/tags')
notice = require('./notice.tmpl')

module.exports = (data) ->
    return ul(
        {className: 'notices col-6'}
        notice(n) for n in data
    )
