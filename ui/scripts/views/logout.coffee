Backbone = require('backbone')
mixins = require('../modules/mixins')

class LogoutView extends Backbone.View
    initialize: (options) ->
        if options.model
            @model = options.model

        if ! @isLoggedIn()
            return Backbone.history.navigate('/', {trigger: true})

        @listenTo(@model, 'logout', @logout)
        @model.logout()

    logout: ->
        window.location = '/'
        # Hard redirect to lose cookie

    isLoggedIn: mixins.isLoggedIn

module.exports = LogoutView
