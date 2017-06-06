const { div, h1, p, a } = require('../../modules/tags')
const notices = require('../components/notices.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = (data) => {
    // TODO-2 update this to use a status field
    if(!data.notices) { return spinner() }

    return div(
        { id: 'notices', className: 'page' },
        h1('Notices'),
        p(a(
            { href: '/follows' },
            icon('follow'),
            ' Manage what I follow'
        )),
        notices(data.notices)
    )
}
