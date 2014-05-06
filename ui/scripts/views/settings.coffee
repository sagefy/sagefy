$ = require('jquery')
FormView = require('./form')
UserModel = require('../models/user')
mixins = require('../modules/mixins')

module.exports = class Settings extends FormView
    title: 'Settings'
    addID: 'settings'
    fields: ['username', 'email']  # password, avatar, notifications
    description: 'All fields autosave.'
    edit: true

    beforeInitialize: ->
        @model = new UserModel({ id: 'current' })

    onRender: ->
        @updatePageWidth(6)

    updatePageWidth: mixins.updatePageWidth
