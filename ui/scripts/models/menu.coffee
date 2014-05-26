Backbone = require('backbone')
$ = require('jquery')
mixins = require('../modules/mixins')

class MenuModel extends Backbone.Model
    menus: {
        loggedOut: [
            'login'
            'terms'
            'contact'
        ]
        loggedIn: [
            'dashboard'
            'inbox'
            'settings'
            'contact'
            'terms'
            'logout'
        ]
    }

    _items: {
        login: { icon: 'sign-in' }
        terms: { icon: 'pencil-square-o' }
        contact: { icon: 'envelope' }
        dashboard: { icon: 'tachometer' }
        inbox: { icon: 'inbox' }
        settings: { icon: 'cog' }
        logout: { icon: 'sign-out' }
    }

    initialize: ->
        @_items = @_itemsBoilerplate(@_items)
        @updateState()

    _itemsBoilerplate: (items = {}) ->
        for name in @_names()
            items[name] = $.extend({
                name: name
                title: @ucfirst(name)
                url: '/' + @underscored(name)
                icon: 'square'
            }, items[name] or {})

        return items

    _names: ->
        names = []

        for menuName, menu of @menus
            for name in menu
                if name not in names
                    names.push(name)

        return names

    updateState: ->
        if @isLoggedIn()
            @state = 'loggedIn'
        else
            @state = 'loggedOut'

        @trigger('changeState', @state)

    items: ->
        return (@_items[name] for name in @menus[@state])

    ucfirst: mixins.ucfirst
    underscored: mixins.underscored
    isLoggedIn: mixins.isLoggedIn

module.exports = MenuModel
