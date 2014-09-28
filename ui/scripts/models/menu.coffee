Model = require('../framework/model')
_ = require('../framework/utilities')
mixins = require('../modules/mixins')

class MenuModel extends Model

    # For each state, a list of the menu items to appear
    menus: {
        loggedOut: [
            'login'
            'terms'
            'contact'
        ]
        loggedIn: [
            'inbox'
            'settings'
            'contact'
            'terms'
            'logout'
        ]
    }

    # A list of all menu items and their configurations
    # The method `_itemBoilerplate` will fill in other values
    _items: {
        login: { icon: 'sign-in' }
        terms: { icon: 'pencil-square-o' }
        contact: { icon: 'envelope' }
        # dashboard: { icon: 'tachometer' }
        inbox: { icon: 'inbox' }
        settings: { icon: 'cog' }
        logout: { icon: 'sign-out' }
    }

    constructor: ->
        super
        # Updates the @_items array with boilerplate
        @_items = @_itemsBoilerplate(@_items)
        # Sets current state
        @updateState()

    # For items that don't have them
    # Use the name to populate title and url automatically
    # And set the default icon to be painfully obviously wrong
    _itemsBoilerplate: (items = {}) ->
        for name in @_names()
            items[name] = _.extend({
                name: name
                title: @ucfirst(name)
                url: '/' + @underscored(name)
                icon: 'square'
            }, items[name] or {})

        return items

    # Generates a list of all menu item names
    _names: ->
        names = []

        for menuName, menu of @menus
            for name in menu
                if name not in names
                    names.push(name)

        return names

    # Determines the state the menu should be in
    # Will vary based on logged in, logged out, and current user page
    updateState: ->
        @state = if @isLoggedIn() then 'loggedIn' else 'loggedOut'
        @trigger('changeState', @state)

    # Returns the list of items for the menu
    # This should be the primary method used by other components
    items: ->
        return (@_items[name] for name in @menus[@state])

    ucfirst: mixins.ucfirst
    underscored: mixins.underscored
    isLoggedIn: mixins.isLoggedIn

module.exports = MenuModel
