define([
    'backbone'
], (Bb) ->

    class PrimaryRouter extends Bb.Router

        routes: {
            'styleguide': 'viewStyleguide'
            'login': 'viewLogin'
            'signup': 'viewSignup'
            'dashboard': 'viewDashboard'
            'terms': 'viewTerms'
            'contact': 'viewContact'
            '(/)': 'viewIndex'
        }

        initialize: ->
            Bb.history.start({pushState: true})

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


)
