const routes = [{
    path: '/sign_up',
    title: 'Sign Up',
}, {
    path: '/log_in',
    title: 'Log In',
}, {
    path: '/password',
    title: 'Password',
}, {
    path: '/styleguide',
    title: 'Styleguide',
}, {
    path: '/terms',
    title: 'Privacy & Terms',
}, {
    path: '/contact',
    title: 'Contact',
}, {
    path: '/settings',
    title: 'Settings',
}, {
    path: '/notices',
    title: 'Notices',
}, {
    path: '/search',
    title: 'Search',
}, {
    path: '/create/set/create',
    title: 'Create a New Set',
}, {
    path: '/create/set/add',
    title: 'Add Existing Members to a Set',
}, {
    path: '/create/unit/find',
    title: 'Find a Set to Add Units',
}, {
    path: '/create/unit/list',
    title: 'Add Units to Set',
}, {
    path: '/create/unit/add',
    title: 'Add Existing Unit to Set',
}, {
    path: '/create/unit/create',
    title: 'Create a New Unit for Set',
}, {
    path: '/create/card/find',
    title: 'Find a Unit to Add Cards',
}, {
    path: '/create/card/list',
    title: 'Add Cards to Unit',
}, {
    path: '/create/card/create',
    title: 'Create a New Card for Unit',
}, {
    path: '/create',
    title: 'Create',
}, {
    path: /^\/topics\/(create|[\d\w]+\/update)$/,
    title: 'Topic',
    // Must be before `topic`
}, {
    path: '/topics/{id}/posts/create',
    title: 'Create Post',
}, {
    path: '/topics/{id}/posts/{id}/update',
    title: 'Update Post'
}, {
    path: '/topics/{id}',
    title: 'Topic',
}, {
    path: '/users/{id}',
    title: 'Profile',
}, {
    path: '/cards/{id}',
    title: 'Card',
}, {
    path: '/units/{id}',
    title: 'Unit',
}, {
    path: '/sets/{id}',
    title: 'Set',
}, {
    path: /^\/(card|unit|set)s\/([\w\d-]+)\/versions$/,
    title: 'Versions',
}, {
    path: '/follows',
    title: 'Follows',
}, {
    path: '/recommended_sets',
    title: 'Recommended Sets',
}, {
    path: '/my_sets',
    title: 'My Sets',
}, {
    path: '/sets/{id}/tree',
    title: 'Set Tree',
}, {
    path: '/sets/{id}/choose_unit',
    title: 'Choose Unit',
}, {
    path: '/cards/{id}/learn',
    title: 'Learn',
}, {
    path: '/sets/{id}/landing',
    title: 'An Introduction to Electronic Music',
}, {
    path: /^\/?$/,
    title: 'Home',
    // Must be 2nd to last
}, {
    path: /.*/,
    title: '404',
    // Must be last
}]

module.exports = routes
