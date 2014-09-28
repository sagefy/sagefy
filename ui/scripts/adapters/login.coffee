PageAdapter = require('./page')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')

class LoginAdapter extends PageAdapter
    url: '/login'
    title: 'Login'

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
            title: 'Login'
            description: '''
                Don't have an account?
                <a href="/signup"><i class="fa fa-user"></i> Signup</a>.
                <br />
                Forgot your password?
                <a href="/password">Reset</a>.
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

module.exports = LoginAdapter
