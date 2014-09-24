PageAdapter = require('./page')
UserModel = require('../models/user')
SignupView = require('../views/signup')

class SignupAdapter extends PageAdapter
    url: '/signup'
    Model: UserModel
    View: SignupView

module.exports = SignupAdapter
