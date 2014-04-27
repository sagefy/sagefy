define([
    'jquery'
    'views/form'
    'models/user'
    'modules/mixins'
], ($, FormView, UserModel, mixins) ->

    class Signup extends FormView

        title: 'Create Account'
        addID: 'signup'
        fields: ['username', 'email', 'password']
        description: '''
            Already have an account?
            <a href="/login"><i class="fa fa-sign-in"></i> Login</a>
        '''
        presubmit: '''
            By signing up,
            you agree to our <a href="/terms">Terms of Service</a>.
        '''
        submitLabel: 'Create Account'
        submitIcon: 'user'

        beforeInitialize: ->
            if @isLoggedIn()
                @onSync()
            @model = new UserModel()

        onSync: ->
            Backbone.history.navigate('/dashboard')

        isLoggedIn: mixins.isLoggedIn


)
