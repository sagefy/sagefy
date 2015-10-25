{div, h1, p, a, i} = require('../../modules/tags')
c = require('../../modules/content').get
notices = require('../components/notices.tmpl')


module.exports = (data) ->
    return div(
        {id: 'notices', className: 'col-6'}
        h1('Notices')
        p(a(
            {href: '/follows'},
            i({className: 'fa fa-cog'})
            ' Manage what I follow'
        ))
        if data.notices \
            then notices(data.notices) \
            else div({className: 'spinner'})
    )
