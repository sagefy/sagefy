FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
util = require('../framework/utilities')

# TODO move copy to content directory

class LogInAdapter extends FormAdapter
    render: ->
        return if @requireLogOut()
        super
        @model = new UserModel()

        @view = new FormLayoutView({
            id: 'log-in'
            className: 'col-6'
            region: @page
        })
        @view.render({
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
        @bindEvents()

    bindEvents: ->
        super
        @listenTo(@model, 'logIn', @toMySets.bind(this))

    getSchema: ->
        return @addModelSchema([{
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
        }])

    toMySets: ->
        # Hard redirect to get the cookie
        window.location = '/my_sets'

    validate: ->
        @model.logIn(@form.getValues())

module.exports = LogInAdapter
