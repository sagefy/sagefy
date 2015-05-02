Store = require('../framework/store')

class UserStore extends Store
    url: (options) ->
        id = options.id or @get('id') or null
        return "/api/users/#{id}/" if id
        return '/api/users/'

    logIn: (data) ->
        return @ajax({
            method: 'POST'
            url: '/api/users/log_in/'
            data: data
            done: =>
                @trigger('logged in user')
            fail: (errors) =>
                @trigger('log in user error', errors)
        })

    logOut: ->
        return @ajax({
            method: 'POST'
            url: '/api/users/log_out/'
            done: =>
                @trigger('logged out user')
            fail: (errors) =>
                @trigger('log out user error', errors)
        })

    getPasswordToken: (data) ->
        return @ajax({
            method: 'POST'
            url: '/api/users/token/'
            data: data
            done: =>
                @trigger('obtained password token')
            fail: (errors) =>
                @trigger('password token error', errors)
        })

    createPassword: (data) ->
        @ajax({
            method: 'POST'
            url: '/api/users/password/'
            data: data
            done: =>
                @trigger('created password')
            fail: (errors) =>
                @trigger('create password error', errors)
        })

module.exports = UserStore
