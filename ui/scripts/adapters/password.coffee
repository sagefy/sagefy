PageAdapter = require('./page')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')

class PasswordAdapter extends PageAdapter
    url: '/password'
    title: 'Create a New Password'

    constructor: ->
        super
        @model = new UserModel()
        @form = new FormView({fields: @getFields()})
        @form.render()
        @view = new FormLayoutView({
            id: 'password'
            className: 'col-6'
            region: @page
        })
        @view.render()
        @view.form.appendChild(@form.el)

    remove: ->
        @view.remove()
        @form.remove()
        @model.remove()
        super

    getFields: ->
        return []

module.exports = PasswordAdapter
