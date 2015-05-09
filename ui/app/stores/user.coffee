Store = require('../framework/store')
userSchema = require('../schemas/user')

class UserStore extends Store
    constructor: ->
        super
        @on('requested log out user', @logOut.bind(this))

    url: (options) ->
        id = options.id or @get('id') or null
        return "/api/users/#{id}/" if id
        return '/api/users/'

    logIn: (data) ->
        return @ajax({
            method: 'POST'
            url: '/api/sessions'
            data: data
            done: =>
                @emit('logged in user')
            fail: (errors) =>
                @emit('log in user error', errors)
        })

    logOut: ->
        return @ajax({
            method: 'DELETE'
            url: '/api/sessions'
            done: =>
                @emit('logged out user')
            fail: (errors) =>
                @emit('log out user error', errors)
        })

    getPasswordToken: (data) ->
        return @ajax({
            method: 'POST'
            url: '/api/password_tokens'
            data: data
            done: =>
                @emit('obtained password token')
            fail: (errors) =>
                @emit('password token error', errors)
        })

    createPassword: (data) ->
        @ajax({
            method: 'POST'
            url: "/api/users/#{data.id}/password"
            data: data
            done: =>
                @emit('created password')
            fail: (errors) =>
                @emit('create password error', errors)
        })

module.exports = UserStore
