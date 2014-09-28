Model = require('../framework/model')

class UserModel extends Model
    url: (options) ->
        id = options.id or @get('id') or null
        return '/api/users/' + (id or '')

    fields: {
        name: {
            type: 'text'
            validations: {
                required: true
            }
        }
        email: {
            type: 'email'
            validations: {
                required: true
                email: true
            }
        }
        password: {
            type: 'password'
            validations: {
                required: true
                minlength: 8
            }
        }
    }

    parse: (response) ->
        return response.user

    login: (data) ->
        return @ajax({
            method: 'POST'
            url: '/api/users/login'
            data: data
            done: =>
                @trigger('login')
            fail: (error) =>
                @trigger('loginError', @parseAjaxErrors(error))
        })

    logout: ->
        return @ajax({
            method: 'POST'
            url: '/api/users/logout'
            done: =>
                @trigger('logout')
        })

    getPasswordToken: (data) ->
        return @ajax({
            method: 'POST'
            url: '/api/users/token'
            data: data
            done: =>
                @trigger('passwordToken')
            fail: (error) =>
                @trigger('errorPasswordToken', @parseAjaxErrors(error))

        })

    createPassword: (data) ->
        @ajax({
            method: 'POST'
            url: '/api/users/password'
            data: data
            done: =>
                @trigger('createPassword')
            fail: (error) =>
                @trigger('errorCreatePassword', @parseAjaxErrors(error))
        })

module.exports = UserModel
