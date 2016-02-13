{ul, p} = require('../../modules/tags')
notice = require('./notice.tmpl')

module.exports = (data) ->
    return p('No notices.') unless data.length
    return ul(
        {className: 'notices'}
        notice(n) for n in data
    )
    # TODO-2 request more notices
