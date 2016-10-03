// TODO-3 move copy to content directory
const {nav, div, a, ul, span} = require('../../modules/tags')
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
    terms: {  },
    contact: { },
    notices: {  },  // TODO-2 poll and show unread count
    settings: {  },
    log_out: { url: '#log_out', title: 'Log Out', icon: 'log-out' },
    search: { },
    current_set: { url: '/sets/{id}/tree', title: 'Current Set', icon: 'set' },
    current_unit: { url: '/units/{id}', title: 'Current Unit', icon: 'unit' },
    discuss_set: {
        url: '/search?kind=topic&q={id}',
        title: 'Discuss Set',
        icon: 'post',
    },
    discuss_unit: {
        url: '/search?kind=topic&q={id}',
        title: 'Discuss Unit',
        icon: 'post',
    },
    discuss_card: {
        url: '/search?kind=topic&q={id}',
        title: 'Discuss Card',
        icon: 'post',
    }
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
        'contact',
        'terms',
    ],
    loggedIn: [
        'my_sets',
        'search',
        'notices',
        'settings',
        'contact',
        'terms',
        'log_out',
    ]
}

const addContextItems = (menuItems, {card, unit, set}) => {
    const add = []
    let discuss, current

    if (set) {
        discuss = extend(items['discuss_set'])
        current = extend(items['current_set'])
        discuss.url = discuss.url.replace('{id}', set)
        current.url = current.url.replace('{id}', set)
        add.push(discuss)
        add.push(current)
    }

    if (unit) {
        discuss = extend(items['discuss_unit'])
        current = extend(items['current_unit'])
        discuss.url = discuss.url.replace('{id}', unit)
        current.url = current.url.replace('{id}', unit)
        add.push(discuss)
        add.push(current)
    }

    if (card) {
        discuss = extend(items['discuss_card'])
        discuss.url = discuss.url.replace('{id}', card)
        add.push(discuss)
    }

    return add.concat(menuItems)
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
