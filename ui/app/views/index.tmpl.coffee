{matchesRoute} = require('../modules/auxiliaries')
{div} = require('../modules/tags')

routes = [
    # ['/sign_up', require('./pages/sign_up.tmpl')]
    # ['/log_in', require('./pages/log_in.tmpl')]
    # ['/log_out', require('./pages/log_out.tmpl')]
    # ['/password', require('./pages/password.tmpl')]
    # ['/styleguide', require('./pages/styleguide.tmpl')]
    # ['/terms', require('./pages/terms.tmpl')]
    # ['/contact', require('./pages/contact.tmpl')]
    # ['/settings', require('./pages/settings.tmpl')]
    # ['/notices', require('./pages/notices.tmpl')]
    # ['/search', require('./pages/search.tmpl')]
    # [
    #     /^\/topics\/(create|[\d\w]+\/update)$/
    #     require('./pages/topic_form.tmpl')
    # ]  # Must be before `topic`
    # [
    #     /^\/posts\/(create|[\d\w]+\/update)$/
    #     require('./pages/post_form.tmpl')
    # ]
    # ['/topics/{id}', require('./pages/topic.tmpl')]
    # ['/cards/{id}', require('./pages/card.tmpl')]
    # ['/units/{id}', require('./pages/unit.tmpl')]
    # ['/sets/{id}', require('./pages/set.tmpl')]
    # ['/follows', require('./pages/follows.tmpl')]
    # ['/my_sets', require('./pages/my_sets.tmpl')]
    # ['/choose_unit', require('./pages/choose_unit.tmpl')]
    # ['/cards/{id}/learn', require('./pages/card_learn.tmpl')]
    [/^\/?$/, require('./pages/home.tmpl')]  # Must be 2nd to last
    [/.*/, require('./pages/error.tmpl')]  # Must be last
]

findRouteTmpl = (data) ->
    for route in routes
        if matchesRoute(data.route, route[0])
            return route[1]

module.exports = (data) ->
    return div(
        {className: 'page'}
        findRouteTmpl(data)(data)
    )
