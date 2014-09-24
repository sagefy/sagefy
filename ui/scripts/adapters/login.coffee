PageAdapter = require('./page')
UserModel = require('../models/user')
LoginView = require('../views/login')

class LoginAdapter extends PageAdapter
    url: '/login'
    Model: UserModel
    View: LoginView

module.exports = LoginAdapter
