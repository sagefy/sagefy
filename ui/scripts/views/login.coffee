$ = require('jquery')
FormView = require('../views/form')
UserModel = require('../models/user')
mixins = require('../modules/mixins')

module.exports = class LoginView extends FormView
    title: 'Login to Sagefy'
    addID: 'login'
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

    beforeInitialize: ->
        if @isLoggedIn()
            return Backbone.history.navigate('/dashboard')

        @model = new UserModel()
        @listenTo(@model, 'login', @login)
        @listenTo(@model, 'loginError', @loginError)

    login: ->
        # Hard redirect to get the cookie
        window.location = '/dashboard'

    loginError: (errors) =>
        @invalid(undefined, errors)

    onRender: ->
        @updatePageWidth(4)

    submit: (e) ->
        e.preventDefault()
        @model.login(@formData(@$form))

    isLoggedIn: mixins.isLoggedIn
    updatePageWidth: mixins.updatePageWidth
