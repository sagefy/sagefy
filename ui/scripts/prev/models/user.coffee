Model = require('../framework/model')

class UserModel extends Model
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
                @trigger('logIn')
            fail: (errors) =>
                @trigger('error', errors)
        })

    logOut: ->
        return @ajax({
            method: 'POST'
            url: '/api/users/log_out/'
            done: =>
                @trigger('logOut')
            fail: (errors) =>
                @trigger('error', errors)
        })

    getPasswordToken: (data) ->
        return @ajax({
            method: 'POST'
            url: '/api/users/token/'
            data: data
            done: =>
                @trigger('passwordToken')
            fail: (errors) =>
                @trigger('error', errors)
        })

    createPassword: (data) ->
        @ajax({
            method: 'POST'
            url: '/api/users/password/'
            data: data
            done: =>
                @trigger('createPassword')
            fail: (errors) =>
                @trigger('error', errors)
        })

module.exports = UserModel
