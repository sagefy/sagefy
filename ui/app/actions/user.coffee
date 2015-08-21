store = require('../modules/store')
ajax = require('../modules/ajax').ajax
mediator = require('../modules/mediator')

module.exports = store.add({
    createUser: (data) ->
        # TODO validate
        # '/api/users/'

    updateUser: (data) ->
        # TODO
        # return "/api/users/#{id}/" if id

    logInUser: (data) ->
        # TODO validate
        return @ajax({
            method: 'POST'
            url: '/api/sessions'
            data: data
            done: ->
                mediator.emit('log in user')
            fail: (errors) ->
                mediator.emit('error on log in user', errors)
        })

    logOutUser: ->
        return @ajax({
            method: 'DELETE'
            url: '/api/sessions'
            done: ->
                mediator.emit('log out user')
            fail: (errors) ->
                mediator.emit('error on log out user', errors)
        })

    getUserPasswordToken: (data) ->
        # TODO validate
        return @ajax({
            method: 'POST'
            url: '/api/password_tokens'
            data: data
            done: ->
                mediator.emit('obtain password token')
            fail: (errors) ->
                mediator.emit('error on password token', errors)
        })

    createUserPassword: (data) ->
        # TODO validate
        return @ajax({
            method: 'POST'
            url: "/api/users/#{data.id}/password"
            data: data
            done: ->
                mediator.emit('create password')
            fail: (errors) ->
                mediator.emit('error on create password', errors)
        })
})
