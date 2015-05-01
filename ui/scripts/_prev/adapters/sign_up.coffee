FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')

# TODO move copy to content directory

class SignUpAdapter extends FormAdapter
    title: 'Sign Up'

    render: ->
        return if @requireLogOut()
        super
        @model = new UserModel()
        @view = new FormLayoutView({
            id: 'sign-up'
            className: 'col-6'
            region: @page
        })
        @view.render({
            title: 'Sign Up for Sagefy'
            description: '''
                Already have an account?
                <a href="/log_in"><i class="fa fa-sign-in"></i> Log In</a>.
                <br />
                By signing up,
                you agree to our <a href="/terms">Terms of Service</a>.
            '''
        })
        @form = new FormView({
            schema: @getSchema()
            region: @view.form
        })
        @form.render()
        @bindEvents()

    bindEvents: ->
        super
        @listenTo(@model, 'sync', @toMySets.bind(this))

    getSchema: ->
        return @addModelSchema([{
            name: 'name'
            label: 'Username'
            placeholder: 'ex: Unicorn'
        }, {
            name: 'email'
            label: 'Email'
            description: 'We need your email to send notices ' +
                         '<br />and reset password.'
            placeholder: 'ex: unicorn@example.com'
        }, {
            name: 'password'
            label: 'Password'
        }, {
            name: 'submit'
            label: 'Sign Up'
            type: 'submit'
            icon: 'user'
        }])

    toMySets: ->
        # Hard redirect to get the cookie
        window.location = '/my_sets'

module.exports = SignUpAdapter
