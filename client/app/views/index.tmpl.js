/* eslint-disable global-require */
const {matchesRoute} = require('../modules/auxiliaries')
const {div, main} = require('../modules/tags')
const {copy} = require('../modules/utilities')

/*
TODO-3 distribute routing, something like...
     module.exports = route(/^\/?$/, 'Home', (data) =>)
*/

const routes = [{
    path: '/sign_up',
    tmpl: require('./pages/sign_up.tmpl'),
}, {
    path: '/log_in',
    tmpl: require('./pages/log_in.tmpl'),
}, {
    path: '/password',
    tmpl: require('./pages/password.tmpl'),
}, {
    path: '/styleguide',
    tmpl: require('./pages/styleguide.tmpl'),
}, {
    path: '/terms',
    tmpl: require('./pages/terms.tmpl'),
}, {
    path: '/contact',
    tmpl: require('./pages/contact.tmpl'),
}, {
    path: '/settings',
    tmpl: require('./pages/settings.tmpl'),
}, {
    path: '/notices',
    tmpl: require('./pages/notices.tmpl'),
}, {
    path: '/search',
    tmpl: require('./pages/search.tmpl'),
}, {
    path: /^\/topics\/(create|[\d\w]+\/update)$/,
    tmpl: require('./pages/topic_form.tmpl'),
    // Must be before `topic`
}, {
    path: '/topics/{id}/posts/create',
    tmpl: require('./pages/post_form.tmpl'),
}, {
    path: '/topics/{id}/posts/{id}/update',
    tmpl: require('./pages/post_form.tmpl'),
}, {
    path: '/topics/{id}',
    tmpl: require('./pages/topic.tmpl'),
}, {
    path: '/users/{id}',
    tmpl: require('./pages/profile.tmpl'),
}, {
    path: '/cards/{id}',
    tmpl: require('./pages/card.tmpl'),
}, {
    path: '/units/{id}',
    tmpl: require('./pages/unit.tmpl'),
}, {
    path: '/sets/{id}',
    tmpl: require('./pages/set.tmpl'),
}, {
    path: /^\/(card|unit|set)s\/([\w\d-]+)\/versions$/,
    tmpl: require('./pages/versions.tmpl'),
}, {
    path: '/follows',
    tmpl: require('./pages/follows.tmpl'),
}, {
    path: '/recommended_sets',
    tmpl: require('./pages/recommended_sets.tmpl'),
}, {
    path: '/my_sets',
    tmpl: require('./pages/my_sets.tmpl'),
}, {
    path: '/sets/{id}/tree',
    tmpl: require('./pages/tree.tmpl'),
}, {
    path: '/sets/{id}/choose_unit',
    tmpl: require('./pages/choose_unit.tmpl'),
}, {
    path: '/cards/{id}/learn',
    tmpl: require('./pages/card_learn.tmpl'),
}, {
    path: /^\/?$/,
    tmpl: require('./pages/home.tmpl'),
    // Must be 2nd to last
}, {
    path: /.*/,
    tmpl: require('./pages/error.tmpl'),
    // Must be last
}]

const findRouteTmpl = (data) => {
    for (let i = 0; i < routes.length; i++) {
        const route = routes[i]
        const args = matchesRoute(data.route, route.path)
        if (args) {
            return [route.tmpl, args]
        }
    }
}

module.exports = (data) => {
    const menuData = copy(data.menu)
    menuData.kind = data.currentUserID ? 'loggedIn' : 'loggedOut'
    const [route, args] = findRouteTmpl(data)
    data = copy(data)
    data.routeArgs = args
    return div(
        main(route(data)),
        require('./components/menu.tmpl')(menuData),
        require('./components/feedback.tmpl')() // TODO-2 Remove this component
    )
}
