FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')

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
        ###
        }, {
            type: 'select'
            field: 'example'
            options: [{
                label: 'A'
                value: 0
            }, {
                label: 'B'
                value: 1
            }, {
                label: 'C'
                value: 2
            }, {
                label: 'D'
                value: 3
            }]
        }])
        ###


    toDashboard: ->
        # Hard redirect to get the cookie
        window.location = '/dashboard'

module.exports = SignupAdapter
