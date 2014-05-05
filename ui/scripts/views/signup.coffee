$ = require('jquery')
FormView = require('views/form')
UserModel = require('models/user')
mixins = require('modules/mixins')

module.exports = class Signup extends FormView
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
            return @onSync()

        @model = new UserModel()

    onSync: ->
        # Hard redirect to get the cookie
        window.location = '/dashboard'

    onRender: ->
        @updatePageWidth(6)

    isLoggedIn: mixins.isLoggedIn
    updatePageWidth: mixins.updatePageWidth
