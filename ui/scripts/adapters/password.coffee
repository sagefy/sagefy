PageAdapter = require('./page')
UserModel = require('../models/user')
# PasswordView = require('../views/password')

class PasswordAdapter extends PageAdapter
    url: '/password'
    title: 'Create a New Password'

    constructor: ->
        super
        @model = new UserModel()
        # @view = new PasswordView()

    remove: ->
        @view.remove()
        @model.remove()
        super

module.exports = PasswordAdapter
