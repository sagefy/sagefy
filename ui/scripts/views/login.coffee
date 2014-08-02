$ = require('jquery')
FormView = require('../views/form')
mixins = require('../modules/mixins')
Backbone = require('backbone')

class LoginView extends FormView
    title: 'Login'
    id: 'login'
    className: 'max-width-4'
    mode: 'create'
    fields: ['name', 'password']
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

        super(options)

        @listenTo(@model, 'login', @login)
        @listenTo(@model, 'loginError', @loginError)

    login: ->
        # Hard redirect to get the cookie
        window.location = '/'

    loginError: (errors) =>
        @displayErrors(errors)

    submit: (e) ->
        if e
            e.preventDefault()
        data = @formData(@$form)
        errors = @model.validate(data, {fields: @fields})
        if errors
            @displayErrors(errors)
        else
            @model.login(@formData(@$form))

    isLoggedIn: mixins.isLoggedIn

module.exports =  LoginView
