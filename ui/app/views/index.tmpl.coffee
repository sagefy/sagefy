{matchesRoute, setTitle} = require('../modules/auxiliaries')
{div, main} = require('../modules/tags')

routes = [
    ['/sign_up', require('./pages/sign_up.tmpl'), 'Sign Up']
    ['/log_in', require('./pages/log_in.tmpl'), 'Log In']
    ['/password', require('./pages/password.tmpl'), 'Password']
    ['/styleguide', require('./pages/styleguide.tmpl'), 'Styleguide']
    ['/terms', require('./pages/terms.tmpl'), 'Privacy & Terms']
    ['/contact', require('./pages/contact.tmpl'), 'Contact']
    ['/settings', require('./pages/settings.tmpl'), 'Settings']
    ['/notices', require('./pages/notices.tmpl'), 'Notices']
    ['/search', require('./pages/search.tmpl'), 'Search']
    [
        /^\/topics\/(create|[\d\w]+\/update)$/
        require('./pages/topic_form.tmpl')
        'Topic'
    ]  # Must be before `topic`
    [
        /^\/posts\/(create|[\d\w]+\/update)$/
        require('./pages/post_form.tmpl')
        'Post'
    ]
    ['/topics/{id}', require('./pages/topic.tmpl'), 'Topic']
    ['/cards/{id}', require('./pages/card.tmpl'), 'Card']
    ['/units/{id}', require('./pages/unit.tmpl'), 'Unit']
    ['/sets/{id}', require('./pages/set.tmpl'), 'Set']
    ['/follows', require('./pages/follows.tmpl'), 'Follow']
    ['/my_sets', require('./pages/my_sets.tmpl'), 'My Sets']
    ['/choose_unit', require('./pages/choose_unit.tmpl'), 'Choose Unit']
    ['/cards/{id}/learn', require('./pages/card_learn.tmpl'), 'Learn']
    [/^\/?$/, require('./pages/home.tmpl'), 'Home']  # Must be 2nd to last
    [/.*/, require('./pages/error.tmpl'), '404']  # Must be last
]

###
TODO distribute routing, something like...
    module.exports = route(/^\/?$/, 'Home', (data) ->)
###

findRouteTmpl = (data) ->
    for route in routes
        if matchesRoute(data.route, route[0])
            setTitle(route[2])
            return route[1]

module.exports = (data) ->
    return div(
        main(
            {className: 'page'}
            findRouteTmpl(data)(data)
        )
        require('./components/menu.tmpl')(data.menu)
    )
