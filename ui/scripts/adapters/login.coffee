FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
_ = require('../framework/utilities')
mixins = require('../modules/mixins')

class LoginAdapter extends FormAdapter
    url: '/login'
    title: 'Log In'
    requireLogout: true

    render: ->
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

        @listenTo(@model, 'login', @toDashboard.bind(this))
        @listenTo(@model, 'error', @error.bind(this))
        @listenTo(@model, 'invalid', @error.bind(this))
        @listenTo(@form, 'submit', @validate.bind(this))
        @listenTo(@form, 'change', @validateField.bind(this))


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
            placeholder: ''
        }, {
            type: 'submit'
            label: 'Log In'
            icon: 'sign-in'
        }]
        for field in fields
            _.extend(field, @model.fields[field.name] or {})
        return fields

    toDashboard: ->
        # Hard redirect to get the cookie
        window.location = '/dashboard'

    error: (errors) ->
        if _.isArray(errors)
            @form.errorMany(errors)
        else
            window.alert(errors)

    validate: ->
        @model.login(@form.getValues())

    validateField: (name, value) ->
        @model.set(name, value)
        error = @model.validateField(name)
        if error
            @form.error(name, {message: error})
        else
            @form.clear(name)

module.exports = LoginAdapter
