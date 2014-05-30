$ = require('jquery')
FormView = require('../views/form')

mixins = require('../modules/mixins')

class Signup extends FormView
    title: 'Create Account'
    id: 'signup'
    className: 'max-width-6'
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

    onSync: ->
        # Hard redirect to get the cookie
        window.location = '/'

    isLoggedIn: mixins.isLoggedIn

module.exports = Signup
