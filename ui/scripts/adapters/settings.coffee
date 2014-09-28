PageAdapter = require('./page')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')

class SettingsAdapter extends PageAdapter
    url: '/settings'
    title: 'Settings'

    constructor: ->
        super
        @model = new UserModel({id: 'current'})
        @form = new FormView({fields: @getFields()})
        @form.render()
        @view = new FormLayoutView()
        @view.render({
            id: 'settings'
            className: 'col-6'
            region: @page
        })
        @view.form.appendChild(@form.el)

    remove: ->
        @view.remove()
        @form.remove()
        @model.remove()
        super

    getFields: ->
        return []

module.exports = SettingsAdapter
