View = require('../../framework/view')
template = require('../../templates/components/menu')
itemTemplate = require('../../templates/components/menu_item')
util = require('../framework/utilities')
aux = require('../modules/auxiliaries')

# A menu component, creates an icon and on click, displays list of options.
class MenuView extends View
    className: 'menu'
    domEvents: {
        'click .menu__overlay': 'toggle'
        'click .menu__trigger': 'toggle'
        'click .menu__item a': 'select'
    }

    # For each state, a list of the menu items to appear
    menus: {
        loggedOut: [
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

    # A list of all menu items and their configurations
    # The method `_itemBoilerplate` will fill in other values
    _items: {
        my_sets: { title: 'My Sets', icon: 'star' }
        log_in: { title: 'Log In', icon: 'sign-in' }
        terms: { icon: 'pencil-square-o' }
        contact: { icon: 'envelope' }
        notices: { icon: 'tachometer' }
        settings: { icon: 'cog' }
        log_out: { title: 'Log Out', icon: 'sign-out' }
    }

    template: template
    itemTemplate: itemTemplate
    selected: false
    ucfirst: aux.ucfirst
    underscored: aux.underscored
    isLoggedIn: aux.isLoggedIn

    constructor: (options) ->
        super
        options.body.appendChild(@el)
        # Updates the @_items array with boilerplate
        @_items = @_itemsBoilerplate(@_items)
        # Sets current state
        @updateState()

    # Render the layout if needed
    # then render data
    render: (data) ->
        @el.innerHTML = @template()
        @renderItems(data)
        @delegateEvents()

    # Produces the data specific HTML
    renderItems: (data) ->
        # Reduce will automatically concat all the template
        # strings for the menu
        html = ''
        for item in data
            html += @itemTemplate(item)
        @el.querySelector('.menu__items').innerHTML = html

    # Open if closed, close if opened
    # Keeps track of own state
    toggle: (e) ->
        if e
            e.preventDefault()
            e.stopPropagation()
        @selected = not @selected
        if @selected
            @el.classList.add('selected')
        else
            @el.classList.remove('selected')

    select: ->
        @toggle()

    # For items that don't have them
    # Use the name to populate title and url automatically
    # And set the default icon to be painfully obviously wrong
    _itemsBoilerplate: (items = {}) ->
        for name in @_names()
            items[name] = util.extend({
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
        @emit('changeState', @state)

    # Returns the list of items for the menu
    # This should be the primary method used by other components
    items: ->
        return (@_items[name] for name in @menus[@state])

module.exports = MenuView
