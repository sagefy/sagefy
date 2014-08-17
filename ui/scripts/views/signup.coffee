$ = require('jquery')
FormView = require('../views/form')
mixins = require('../modules/mixins')

class Signup extends FormView
    title: 'Create Account'
    id: 'signup'
    className: 'col-6'
    mode: 'create'
    fields: ['name', 'email', 'password']
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

    initialize: (options) ->
        if @isLoggedIn()
            return @sync()

        super(options)

    sync: ->
        # Hard redirect to get the cookie
        window.location = '/'

    isLoggedIn: mixins.isLoggedIn

module.exports = Signup
