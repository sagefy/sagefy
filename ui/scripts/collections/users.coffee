Backbone = require('backbone')
UserModel = require('models/user')

module.exports = class UsersCollection extends Backbone.UsersCollection
    model: UserModel
