FormPageView = require('./_form')
FormView = require('../components/form')
aux = require('../../modules/auxiliaries')
userSchema = require('../../schemas/user.coffee')

class LogInPageView extends FormPageView
    id: 'log-in'
    className: 'col-6'

    schema: [{
        name: 'name'
        label: 'Username'
        placeholder: 'e.g. Unicorn'
    }, {
        name: 'password'
        label: 'Password'
        placeholder: ''
    }, {
        type: 'submit'
        name: 'log-in'
        label: 'Log In'
        icon: 'sign-in'
    }]

    constructor: ->
        super
        aux.setTitle('Log In')
        # If the user is already logged in, redirect to my sets
        @render({
            title: 'Log In to Sagefy'
            description: '''
                Don't have an account?
                <a href="/sign_up"><i class="fa fa-user"></i> Sign Up</a>.
                <br />
                Forgot your password?
                <a href="/password"><i class="fa fa-refresh"></i> Reset</a>.
            '''
        })

        @form = new FormView({
            schema: @getSchema()
            region: @view.form
        })
        @form.render()

        # @listenTo(@model, 'logIn', @toMySets.bind(this))

    validate: ->
        # @model.logIn(@form.getValues())

module.exports = LogInPageView
