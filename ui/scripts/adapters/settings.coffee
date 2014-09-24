PageAdapter = require('./page')
UserModel = require('../models/user')
SettingsView = require('../views/settings')

class SettingsAdapter extends PageAdapter
    url: '/settings'
    Model: UserModel
    View: SettingsView
    modelOptions: {id: 'current'}

module.exports = SettingsAdapter
