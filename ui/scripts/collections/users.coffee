Backbone = require('backbone')
UserModel = require('../models/user')

class UsersCollection extends Backbone.UsersCollection
    model: UserModel

module.exports = UsersCollection
