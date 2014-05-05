Bb = require('backbone')
mixins = require('modules/mixins')
UserModel = require('models/user')

module.exports = class LogoutView extends Bb.View
    initialize: ->
        if ! @isLoggedIn()
            return Backbone.history.navigate('/', {trigger: true})

        @model = new UserModel({id: 'current'})
        @model.on('logout', @logout)
        @model.logout()

    logout: ->
        window.location = '/'
        # Hard redirect to lose cookie

    isLoggedIn: mixins.isLoggedIn
