Backbone = require('backbone')
UserModel = require('../models/user')

class UsersCollection extends Backbone.Collection
    model: UserModel

module.exports = UsersCollection
