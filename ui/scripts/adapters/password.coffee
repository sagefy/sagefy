PageAdapter = require('./page')
UserModel = require('../models/user')
PasswordView = require('../views/password')

class PasswordAdapter extends PageAdapter
    url: '/password'
    Model: UserModel
    View: PasswordView

module.exports = PasswordAdapter
