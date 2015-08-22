aux = require('../modules/auxiliaries')
{matchesRoute} = require('../modules/tags')

routes = [
    ['/sign_up', require('./views/pages/sign_up.tmpl')]
    ['/log_in', require('./views/pages/log_in.tmpl')]
    ['/log_out', require('./views/pages/log_out.tmpl')]
    ['/password', require('./views/pages/password.tmpl')]
    ['/styleguide', require('./views/pages/styleguide.tmpl')]
    ['/terms', require('./views/pages/terms.tmpl')]
    ['/contact', require('./views/pages/contact.tmpl')]
    ['/settings', require('./views/pages/settings.tmpl')]
    ['/notices', require('./views/pages/notices.tmpl')]
    ['/search', require('./views/pages/search.tmpl')]
    [
        /^\/topics\/(create|[\d\w]+\/update)$/
        require('./views/pages/topic_form.tmpl')
    ]  # Must be before `topic`
    [
        /^\/posts\/(create|[\d\w]+\/update)$/
        require('./views/pages/post_form.tmpl')
    ]
    ['/topics/{id}', require('./views/pages/topic.tmpl')]
    ['/cards/{id}', require('./views/pages/card.tmpl')]
    ['/units/{id}', require('./views/pages/unit.tmpl')]
    ['/sets/{id}', require('./views/pages/set.tmpl')]
    ['/follows', require('./views/pages/follows.tmpl')]
    ['/my_sets', require('./views/pages/my_sets.tmpl')]
    ['/choose_unit', require('./views/pages/choose_unit.tmpl')]
    ['/cards/{id}/learn', require('./views/pages/card_learn.tmpl')]
    [/^\/?$/, require('./views/pages/home.tmpl')]  # Must be 2nd to last
    [/.*/, require('./views/pages/error.tmpl')]  # Must be last
]

findRouteTmpl = (data) ->
    for route in routes
        if matchesRoute(data.route, route[0])
            return route[1]

module.exports = (data) ->
    return div(
        {className: 'page'}
        findRouteTmpl(data)
    )
