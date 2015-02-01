FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
util = require('../framework/utilities')

# TODO: move copy to content directory

class LoginAdapter extends FormAdapter
    url: '/login'
    title: 'Log In'

    render: ->
        return if @requireLogout()
        super
        @model = new UserModel()
        @form = new FormView({schema: @getSchema()})
        @form.render()
        @view = new FormLayoutView({
            id: 'login'
            className: 'col-6'
            region: @page
        })
        @view.render({
            title: 'Log In to Sagefy'
            description: '''
                Don't have an account?
                <a href="/signup"><i class="fa fa-user"></i> Sign Up</a>.
                <br />
                Forgot your password?
                <a href="/password"><i class="fa fa-refresh"></i> Reset</a>.
            '''
        })
        @view.form.appendChild(@form.el)

        @bindEvents()

    bindEvents: ->
        super
        @listenTo(@model, 'login', @toDashboard.bind(this))

    getSchema: ->
        return @addModelSchema([{
            name: 'name'
            title: 'Username'
            placeholder: 'e.g. Unicorn'
        }, {
            name: 'password'
            title: 'Password'
            placeholder: ''
        }, {
            type: 'submit'
            label: 'Log In'
            icon: 'sign-in'
        }])

    toDashboard: ->
        # Hard redirect to get the cookie
        window.location = '/dashboard'

    validate: ->
        @model.login(@form.getValues())

module.exports = LoginAdapter
