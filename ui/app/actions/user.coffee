store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

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
                recorder.emit('log in user')
            fail: (errors) ->
                recorder.emit('error on log in user', errors)
        })

    logOutUser: ->
        return @ajax({
            method: 'DELETE'
            url: '/api/sessions'
            done: ->
                window.location = '/'  # Hard refresh for cookie
                recorder.emit('log out user')
            fail: (errors) ->
                recorder.emit('error on log out user', errors)
        })

    getUserPasswordToken: (data) ->
        # TODO validate
        return @ajax({
            method: 'POST'
            url: '/api/password_tokens'
            data: data
            done: ->
                recorder.emit('obtain password token')
            fail: (errors) ->
                recorder.emit('error on password token', errors)
        })

    createUserPassword: (data) ->
        # TODO validate
        return @ajax({
            method: 'POST'
            url: "/api/users/#{data.id}/password"
            data: data
            done: ->
                recorder.emit('create password')
            fail: (errors) ->
                recorder.emit('error on create password', errors)
        })
})
