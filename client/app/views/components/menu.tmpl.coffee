# TODO move copy to content directory
{nav, div, a, i, ul} = require('../../modules/tags')
menuItem = require('./menu_item.tmpl')
{extend} = require('../../modules/utilities')
{ucfirst, underscored} = require('../../modules/auxiliaries')


# TODO add unread count to notices icon


# A list of all menu items and their configurations
items = {
    home: { url: '/' }
    my_sets: { title: 'My Sets', icon: 'star' }
    log_in: { title: 'Log In', icon: 'sign-in' }
    terms: { icon: 'pencil-square-o' }
    contact: { icon: 'envelope' }
    notices: { icon: 'tachometer' }   # TODO poll and show unread count
    settings: { icon: 'cog' }
    log_out: { url: '#log_out', title: 'Log Out', icon: 'sign-out' }
    search: { }
}

# For items that don't have them
# Use the name to populate title and url automatically
# And set the default icon to be painfully obviously wrong
for name, item of items
    items[name] = extend({
        name: name
        title: ucfirst(name)
        url: '/' + underscored(name)
        icon: name
    }, items[name] or {})

# For each state, a list of the menu items to appear
menus = {
    loggedOut: [
        'home'
        'log_in'
        'contact'
        'terms'
    ]
    loggedIn: [
        'my_sets'
        'search'
        'notices'
        'settings'
        'contact'
        'terms'
        'log_out'
    ]
}

module.exports = (data) ->
    menuItems = menus[data.kind].map((name) -> items[name])
    return nav(
        {className: if data.open then 'menu selected' else 'menu'}
        [
            div(
                {className: 'menu__overlay'}
            ) if data.open
            a(
                {
                    href: '#'
                    className: 'menu__trigger'
                    'data-title': 'Menu'
                }
                div({className: 'menu__logo'})
                i({className: 'menu__close fa fa-times-circle'}) if data.open
            )
            ul(
                {className: 'menu__items'}
                menuItem(d) for d in menuItems
            ) if data.open
        ]
    )
