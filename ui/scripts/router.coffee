Backbone = require('backbone')
$ = require('jquery')
MenuGlobalView = require('./views/menu--global')
StyleguideView = require('./views/styleguide')
LoginView = require('./views/login')
LogoutView = require('./views/logout')
TermsView = require('./views/terms')
DashboardView = require('./views/dashboard')
TermsView = require('./views/terms')
ContactView = require('./views/contact')
SettingsView = require('./views/settings')
IndexView = require('./views/index')
SignupView = require('./views/signup')
CreatePasswordView = require('./views/create_password')

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
        'create_password': 'createPassword'
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

    viewIndex: ->
        view = new IndexView()

    viewLogin: ->
        view = new LoginView()

    viewLogout: ->
        view = new LogoutView()

    viewSignup: ->
        view = new SignupView()

    viewTerms: ->
        view = new TermsView()

    viewContact: ->
        view = new ContactView()

    viewStyleguide: ->
        view = new StyleguideView()

    viewDashboard: ->
        view = new DashboardView()

    viewSettings: ->
        view = new SettingsView()

    createPassword: ->
        view = new CreatePasswordView()
