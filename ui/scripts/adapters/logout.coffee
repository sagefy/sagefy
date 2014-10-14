PageAdapter = require('./page')
UserModel = require('../models/user')
utilities = require('../modules/utilities')

# TODO: trans

class LogoutAdapter extends PageAdapter
    url: '/logout'
    title: 'Logging out...'

    render: ->
        super
        if utilities.isLoggedIn()
            @model = new UserModel({
                id: 'current'
            })
            @listenTo(@model, 'logout', @toIndex)
            @model.logout()
        else
            @toIndex()

    remove: ->
        @model.remove()
        super

    # Hard redirect to lose cookie
    toIndex: ->
        window.location = '/'

module.exports = LogoutAdapter
