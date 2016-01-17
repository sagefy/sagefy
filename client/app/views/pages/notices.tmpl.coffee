{div, h1, p, a, i} = require('../../modules/tags')
c = require('../../modules/content').get
notices = require('../components/notices.tmpl')
spinner = require('../components/spinner.tmpl')


module.exports = (data) ->
    return spinner() unless data.notices

    return div(
        {id: 'notices'}
        h1('Notices')
        p(a(
            {href: '/follows'},
            i({className: 'fa fa-cog'})
            ' Manage what I follow'
        ))
        notices(data.notices)
    )
