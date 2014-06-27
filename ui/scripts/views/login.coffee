$ = require('jquery')
FormView = require('../views/form')
mixins = require('../modules/mixins')

class LoginView extends FormView
    title: 'Login to Sagefy'
    id: 'login'
    className: 'max-width-4'
    fields: ['username', 'password']
    description: '''
        Don't have an account?
        <a href="/signup"><i class="fa fa-user"></i> Signup</a>
    '''
    presubmit: '''
        Forgot your password?
        <a href="/create_password">Create a new password</a>
    '''
    submitLabel: 'Login'
    submitIcon: 'sign-in'

    initialize: (options) ->
        if @isLoggedIn()
            return Backbone.history.navigate('/')

        @listenTo(@model, 'login', @login)
        @listenTo(@model, 'loginError', @loginError)

        super(options)

    login: ->
        # Hard redirect to get the cookie
        window.location = '/'

    loginError: (errors) =>
        @invalid(undefined, errors)

    submit: (e) ->
        if e
            e.preventDefault()
        data = @formData(@$form)
        @model.viewFields = @fields  # TODO: this is bad
        errors = @model.validate(data)
        @model.viewFields = null
        if errors
            @displayErrors(errors)
        else
            @model.login(@formData(@$form))

    isLoggedIn: mixins.isLoggedIn

module.exports =  LoginView
