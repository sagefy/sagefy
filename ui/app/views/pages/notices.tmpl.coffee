{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
notices = require('../components/notices.tmpl')

# TODO@ include a link to follows

module.exports = (data) ->
    return div(
        {id: 'notices', className: 'col-6'}
        h1('Notices')
        if data.notices \
            then notices(data.notices) \
            else div({className: 'spinner'})
    )
