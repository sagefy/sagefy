// TODO-3 move copy to content directory
const {nav, div, a, ul, span, p} = require('../../modules/tags')
const menuItem = require('./menu_item.tmpl')
const {extend} = require('../../modules/utilities')
const {ucfirst, underscored} = require('../../modules/auxiliaries')
const icon = require('./icon.tmpl')

// TODO-2 add unread count to notices icon

// A list of all menu items and their configurations
const items = {
    home: { url: '/' },
    my_sets: { title: 'My Sets', icon: 'set' },
    log_in: { title: 'Log In', icon: 'log-in' },
    terms: { },
    contact: { },
    notices: { },  // TODO-2 poll and show unread count
    settings: { },
    log_out: { url: '#log_out', title: 'Log Out', icon: 'log-out' },
    search: { },
    discuss_card: {
        url: '/search?kind=topic&q={id}',
        title: 'Discuss Card',
        icon: 'post',
    },
    discuss_unit: {
        url: '/search?kind=topic&q={id}',
        title: 'Discuss Unit',
        icon: 'post',
    },
    discuss_set: {
        url: '/search?kind=topic&q={id}',
        title: 'Discuss Set',
        icon: 'post',
    },
    create: { }
}

// For items that don't have them
// Use the name to populate title and url automatically
// And set the default icon to be painfully obviously wrong
Object.keys(items).forEach(name => {
    items[name] = extend({
        name: name,
        title: ucfirst(name),
        url: '/' + underscored(name),
        icon: name,
    }, items[name] || {})
})

// For each state, a list of the menu items to appear
const menus = {
    loggedOut: [
        'home',
        'log_in',
        'search',
        'contact',
        'terms',
    ],
    loggedIn: [
        'my_sets',
        'search',
        'notices',
        // 'create',
        'settings',
        'contact',
        'terms',
        'log_out',
    ]
}

const addContextItems = (menuItems /* , TP@ {card, unit, set} */) => {
    menuItems = menuItems.slice()

    /* TP@
    if (card) {
        const discuss = extend(items.discuss_card)
        discuss.url = discuss.url.replace('{id}', card)
        menuItems.push(discuss)
        return menuItems
    }

    if (unit) {
        const discuss = extend(items.discuss_unit)
        discuss.url = discuss.url.replace('{id}', unit)
        menuItems.push(discuss)
        return menuItems
    }

    if (set) {
        const discuss = extend(items.discuss_set)
        discuss.url = discuss.url.replace('{id}', set)
        menuItems.push(discuss)
        return menuItems
    }
    */

    return menuItems
}

module.exports = (data) => {
    let menuItems = menus[data.kind].map((name) => items[name])
    menuItems = addContextItems(menuItems, data.context)
    return nav(
        {className: data.open ? 'menu selected' : 'menu'},
        [
            data.open ? div(
                {className: 'menu__overlay'}
            ) : null,
            a(
                {
                    href: '#',
                    className: 'menu__trigger',
                },
                div({className: 'menu__logo'}),
                p({className: 'menu__label'}, 'Menu'),
                data.open ?
                    span({className: 'menu__close'}, icon('remove')) :
                    null
            ),
            data.open ? ul(
                {className: 'menu__items'},
                menuItems.map(d => menuItem(d))
            ) : null
        ]
    )
}
