PageAdapter = require('./page')
UserModel = require('../models/user')
aux = require('../modules/auxiliaries')

# TODO move copy to content directory

class LogOutAdapter extends PageAdapter
    title: 'Logging out...'

    render: ->
        super
        if aux.isLoggedIn()
            @model = new UserModel({
                id: 'current'
            })
            @listenTo(@model, 'logOut', @toIndex)
            @model.logOut()
        else
            @toIndex()

    remove: ->
        @model.remove()
        super

    # Hard redirect to lose cookie
    toIndex: ->
        window.location = '/'

module.exports = LogOutAdapter
