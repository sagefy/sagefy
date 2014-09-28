PageAdapter = require('./page')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')

class SignupAdapter extends PageAdapter
    url: '/signup'
    title: 'Create Account'

    constructor: ->
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
            title: 'Signup'
            description: '''
                Already have an account?
                <a href="/login"><i class="fa fa-sign-in"></i> Login</a>.
                <br />
                By signing up,
                you agree to our <a href="/terms">Terms of Service</a>.
            '''
        })
        @view.form.appendChild(@form.el)

    remove: ->
        @view.remove()
        @form.remove()
        @model.remove()
        super

    getFields: ->
        return []

module.exports = SignupAdapter
