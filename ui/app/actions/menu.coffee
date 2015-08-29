store = require('../modules/store')
recorder = require('../modules/recorder')
{extend} = require('../modules/utilities')
{ucfirst, underscored} = require('../modules/auxiliaries')

store.init(->
    # TODO@ Derivative data should be created in the view layer,
    #       not the store unless there is a significant CPU
    #       concern

    @data.menu = {open: false}

    # A list of all menu items and their configurations
    items = {
        home: { url: '/' }
        my_sets: { title: 'My Sets', icon: 'star' }
        log_in: { title: 'Log In', icon: 'sign-in' }
        terms: { icon: 'pencil-square-o' }
        contact: { icon: 'envelope' }
        notices: { icon: 'tachometer' }
        settings: { icon: 'cog' }
        log_out: { title: 'Log Out', icon: 'sign-out' }
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
            'notices'
            'settings'
            'contact'
            'terms'
            'log_out'
        ]
    }

    @data.menu.items = menus.loggedOut.map((name) -> items[name])
)

module.exports = store.add({
    toggleMenu: ->
        @data.menu.open = not @data.menu.open
        recorder.emit('toggle menu',
            if @data.menu.open then 'open' else 'closed')
        @change()
})
