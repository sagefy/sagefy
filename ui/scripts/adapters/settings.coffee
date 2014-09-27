PageAdapter = require('./page')
UserModel = require('../models/user')
# SettingsView = require('../views/settings')

class SettingsAdapter extends PageAdapter
    url: '/settings'
    title: 'Settings'

    constructor: ->
        super
        @model = new UserModel({id: 'current'})
        # @view = new SettingsView()

    remove: ->
        @view.remove()
        @model.remove()
        super

module.exports = SettingsAdapter
