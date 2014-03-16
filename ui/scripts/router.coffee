define([
    'backbone'
    'modules/init'
], (Bb, init) ->

    class PrimaryRouter extends Bb.Router

        routes: {
            'styleguide': 'viewStyleguide'
            'login': 'viewLogin'
            'signup': 'viewSignup'
            'terms': 'viewTerms'
            'contact': 'viewContact'
            '(/)': 'viewIndex'
        }

        initialize: ->
            init.configFormValidation()
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


)
