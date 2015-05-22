Store = require('../modules/store')
userSchema = require('../schemas/user')

class UserStore extends Store
    constructor: ->
        super
        @on('request log out user', @logOut.bind(this))
        @on('request log in user', @logIn.bind(this))
        @on('request create user', @create.bind(this))

    url: (options) ->
        id = options.id or @get('id') or null
        return "/api/users/#{id}/" if id
        return '/api/users/'

    create: (data) ->
        # TODO validate

    logIn: (data) ->
        # TODO validate
        return @ajax({
            method: 'POST'
            url: '/api/sessions'
            data: data
            done: =>
                @emit('log in user')
            fail: (errors) =>
                @emit('error on log in user', errors)
        })

    logOut: ->
        return @ajax({
            method: 'DELETE'
            url: '/api/sessions'
            done: =>
                @emit('log out user')
            fail: (errors) =>
                @emit('error on log out user', errors)
        })

    getPasswordToken: (data) ->
        # TODO validate
        return @ajax({
            method: 'POST'
            url: '/api/password_tokens'
            data: data
            done: =>
                @emit('obtain password token')
            fail: (errors) =>
                @emit('error on password token', errors)
        })

    createPassword: (data) ->
        # TODO validate
        return @ajax({
            method: 'POST'
            url: "/api/users/#{data.id}/password"
            data: data
            done: =>
                @emit('create password')
            fail: (errors) =>
                @emit('error on create password', errors)
        })

module.exports = UserStore
