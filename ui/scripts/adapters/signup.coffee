FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
utilities = require('../modules/utilities')
util = require('../framework/utilities')

# TODO: move copy to content directory

class SignupAdapter extends FormAdapter
    url: '/signup'
    title: 'Sign Up'

    render: ->
        return if @requireLogout()
        super
        @model = new UserModel()
        @form = new FormView({schema: @getSchema()})
        @form.render()
        @view = new FormLayoutView({
            id: 'signup'
            className: 'col-6'
            region: @page
        })
        @view.render({
            title: 'Sign Up for Sagefy'
            description: '''
                Already have an account?
                <a href="/login"><i class="fa fa-sign-in"></i> Login</a>.
                <br />
                By signing up,
                you agree to our <a href="/terms">Terms of Service</a>.
            '''
        })
        @view.form.appendChild(@form.el)
        @bindEvents()

    bindEvents: ->
        super
        @listenTo(@model, 'sync', @toDashboard.bind(this))

    getSchema: ->
        return @addModelSchema([{
            name: 'name'
            title: 'Username'
            placeholder: 'ex: Unicorn'
        }, {
            name: 'email'
            title: 'Email'
            description: 'We need your email to send notices ' +
                         '<br />and reset password.'
            placeholder: 'ex: unicorn@example.com'
        }, {
            name: 'password'
            title: 'Password'
        }, {
            type: 'submit'
            label: 'Sign Up'
            icon: 'user'
        }])

    toDashboard: ->
        # Hard redirect to get the cookie
        window.location = '/dashboard'

module.exports = SignupAdapter
