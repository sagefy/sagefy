FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
utilities = require('../modules/utilities')
_ = require('../framework/utilities')

# TODO: move copy to content directory

class SignupAdapter extends FormAdapter
    url: '/signup'
    title: 'Sign Up'
    requireLogout: true

    render: ->
        super
        @model = new UserModel()
        @form = new FormView({fields: @getFields()})
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

        @listenTo(@model, 'invalid', @error.bind(this))
        @listenTo(@model, 'error', @error.bind(this))
        @listenTo(@model, 'sync', @toDashboard.bind(this))
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
        @model.set(@form.getValues())
        @model.save()

    validateField: (name, value) ->
        @model.set(name, value)
        error = @model.validateField(name)
        if error
            @form.error(name, {message: error})
        else
            @form.clear(name)

module.exports = SignupAdapter
