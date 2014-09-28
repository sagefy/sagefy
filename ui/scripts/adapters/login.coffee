PageAdapter = require('./page')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
_ = require('../framework/utilities')

class LoginAdapter extends PageAdapter
    url: '/login'
    title: 'Log In'

    constructor: ->
        super
        @model = new UserModel()
        @form = new FormView({fields: @getFields()})
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

    remove: ->
        @view.remove()
        @form.remove()
        @model.remove()
        super

    getFields: ->
        fields = [{
            name: 'name'
            title: 'Username'
            placeholder: 'e.g. Unicorn'
        }, {
            name: 'password'
            title: 'Password'
        }, {
            type: 'submit'
            label: 'Log In'
            icon: 'sign-in'
        }]
        for field in fields
            _.extend(field, @model.fields[field.name] or {})
        return fields

module.exports = LoginAdapter
