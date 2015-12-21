{matchesRoute, setTitle} = require('../modules/auxiliaries')
{div, main} = require('../modules/tags')
{copy} = require('../modules/utilities')

###
TODO distribute routing, something like...
     module.exports = route(/^\/?$/, 'Home', (data) ->)
###

routes = [{
    path: '/sign_up'
    tmpl: require('./pages/sign_up.tmpl')
    title: 'Sign Up'
}, {
    path: '/log_in'
    tmpl: require('./pages/log_in.tmpl')
    title: 'Log In'
}, {
    path: '/password'
    tmpl: require('./pages/password.tmpl')
    title: 'Password'
}, {
    path: '/styleguide'
    tmpl: require('./pages/styleguide.tmpl')
    title: 'Styleguide'
}, {
    path: '/terms'
    tmpl: require('./pages/terms.tmpl')
    title: 'Privacy & Terms'
}, {
    path: '/contact'
    tmpl: require('./pages/contact.tmpl')
    title: 'Contact'
}, {
    path: '/settings'
    tmpl: require('./pages/settings.tmpl')
    title: 'Settings'
}, {
    path: '/notices'
    tmpl: require('./pages/notices.tmpl')
    title: 'Notices'
}, {
    path: '/search'
    tmpl: require('./pages/search.tmpl')
    title: 'Search'
}, {
    path: /^\/topics\/(create|[\d\w]+\/update)$/
    tmpl: require('./pages/topic_form.tmpl')
    title: 'Topic'
    # Must be before `topic`
}, {
    path: '/topics/{id}/posts/create'
    tmpl: require('./pages/post_form.tmpl')
    title: 'Create Post'
}, {
    path: '/topics/{id}/posts/{id}/update'
    tmpl: require('./pages/post_form.tmpl')
    title: 'Update Post'
}, {
    path: '/topics/{id}'
    tmpl: require('./pages/topic.tmpl')
    title: 'Topic'
}, {
    path: '/users/{id}'
    tmpl: require('./pages/profile.tmpl')
    title: 'Profile'
}, {
    path: '/cards/{id}'
    tmpl: require('./pages/card.tmpl')
    title: 'Card'
}, {
    path: '/units/{id}'
    tmpl: require('./pages/unit.tmpl')
    title: 'Unit'
}, {
    path: '/sets/{id}'
    tmpl: require('./pages/set.tmpl')
    title: 'Set'
}, {
    path: /^\/(card|unit|set)s\/([\w\d-]+)\/versions$/
    tmpl: require('./pages/versions.tmpl')
    title: 'Versions'
}, {
    path: '/follows'
    tmpl: require('./pages/follows.tmpl')
    title: 'Follows'
}, {
    path: '/my_sets'
    tmpl: require('./pages/my_sets.tmpl')
    title: 'My Sets'
}, {
    path: '/sets/{id}/tree'
    tmpl: require('./pages/tree.tmpl')
    title: 'Set Tree'
}, {
    path: '/sets/{id}/choose_unit'
    tmpl: require('./pages/choose_unit.tmpl')
    title: 'Choose Unit'
}, {
    path: '/cards/{id}/learn'
    tmpl: require('./pages/card_learn.tmpl')
    title: 'Learn'
}, {
    path: /^\/?$/
    tmpl: require('./pages/home.tmpl')
    title: 'Home'
    # Must be 2nd to last
}, {
    path: /.*/
    tmpl: require('./pages/error.tmpl')
    title: '404'
    # Must be last
}]

findRouteTmpl = (data) ->
    for route in routes
        if args = matchesRoute(data.route, route.path)
            setTitle(route.title)
            return [route.tmpl, args]

module.exports = (data) ->
    menuData = copy(data.menu)
    menuData.kind = if data.currentUserID then 'loggedIn' else 'loggedOut'

    [route, args] = findRouteTmpl(data)
    data = copy(data)
    data.routeArgs = args

    return div(
        main(
            {className: 'page'}
            route(data)
        )
        require('./components/menu.tmpl')(menuData)
    )
