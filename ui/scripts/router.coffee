Backbone = require('backbone')
MenuGlobalView = require('./views/menu--global')
StyleguideView = require('./views/styleguide')

module.exports = class PrimaryRouter extends Backbone.Router
    routes: {
        'styleguide': 'viewStyleguide'
        'login': 'viewLogin'
        'logout': 'viewLogout'
        'signup': 'viewSignup'
        'dashboard': 'viewDashboard'
        'terms': 'viewTerms'
        'contact': 'viewContact'
        'settings': 'viewSettings'
        '(/)': 'viewIndex'
    }

    initialize: ->
        Backbone.history.start({pushState: true})
        menuGlobalView = new MenuGlobalView()

        # When we click an internal link, use Navigate instead
        $('body').on('click', 'a[href^="/"]', (e) ->
            e.preventDefault()
            href = $(e.currentTarget).closest('a').attr('href')
            Backbone.history.navigate(href, {trigger: true})
        )

    _view: (type) ->
        require(['views/' + type], (View) ->
            view = new View
        )

    viewIndex: ->
        @_view('index')

    viewLogin: ->
        @_view('login')

    viewLogout: ->
        @_view('logout')

    viewSignup: ->
        @_view('signup')

    viewTerms: ->
        @_view('terms')

    viewContact: ->
        @_view('contact')

    viewStyleguide: ->
        @_view('styleguide')

    viewDashboard: ->
        @_view('dashboard')

    viewSettings: ->
        @_view('settings')
