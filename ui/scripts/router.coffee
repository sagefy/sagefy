define([
    'backbone'
    'views/menu--global'
], (Backbone, MenuGlobalView) ->

    class PrimaryRouter extends Backbone.Router

        routes: {
            'styleguide': 'viewStyleguide'
            'login': 'viewLogin'
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

        viewIndex: ->
            require(['views/index'], (IndexView) ->
                indexView = new IndexView
            )

        viewLogin: ->
            require(['views/login'], (LoginView) ->
                loginView = new LoginView
            )

        viewSignup: ->
            require(['views/signup'], (SignupView) ->
                signupView = new SignupView
            )

        viewTerms: ->
            require(['views/terms'], (TermsView) ->
                termsView = new TermsView
            )

        viewContact: ->
            require(['views/contact'], (ContactView) ->
                contactView = new ContactView
            )

        viewStyleguide: ->
            require(['views/styleguide'], (StyleguideView) ->
                styleguideView = new StyleguideView
            )

        viewDashboard: ->
            require(['views/dashboard'], (DashboardView) ->
                dashboardView = new DashboardView
            )

        viewSettings: ->
            require(['views/settings'], (SettingsView) ->
                settingsView = new SettingsView
            )

)
