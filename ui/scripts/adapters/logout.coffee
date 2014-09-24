PageAdapter = require('./page')
UserModel = require('../models/user')
LogoutView = require('../views/logout')

class LogoutAdapter extends PageAdapter
    url: '/logout'
    Model: UserModel
    View: LogoutView
    modelOptions: {id: 'current'}

module.exports = LogoutAdapter
