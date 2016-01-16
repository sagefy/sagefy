store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
cookie = require('../modules/cookie')

# TODO-2 move setting and unsetting of currentUserID back to the server

module.exports = store.add({
    createUser: (data) ->
        @data.sending = true
        @change()
        recorder.emit('create user')
        ajax({
            method: 'POST'
            url: '/s/users'
            data: data
            done: (response) =>
                @data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('create user success')
                window.location = '/my_sets'
                # Hard redirect to get the HTTP_ONLY cookie
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on create user', errors)
            always: =>
                @data.sending = false
                @change()
        })

    updateUser: (data) ->
        @data.sending = true
        @change()
        recorder.emit('update user', response.user.id)
        ajax({
            method: 'PUT'
            url: "/s/users/#{data.id}"
            data: data
            done: (response) =>
                @data.users ?= {}
                @data.users[response.user.id] = response.user
                recorder.emit('update user success', response.user.id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('update user failure', errors)
            always: =>
                @data.sending = false
                @change()
        })

    getCurrentUser: ->
        recorder.emit('get current user')
        ajax({
            method: 'GET'
            url: '/s/users/current'
            done: (response) =>
                @data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                @data.users ?= {}
                @data.users[response.user.id] = response.user
                recorder.emit('get current user success')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('get current user failure', errors)
            always: =>
                @change()
        })

    getUser: (id, opts = {}) ->
        recorder.emit('get user', id)
        ajax({
            method: 'GET'
            url: "/s/users/#{id}"
            data: opts
            done: (response) =>
                @data.users ?= {}
                user = response.user
                ['avatar', 'posts', 'sets', 'follows'].forEach((t) ->
                    user[t] = response[t] if response[t]
                )
                @data.users[response.user.id] = user
                recorder.emit('get user success', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('get user failure', id, errors)
            always: =>
                @change()
        })

    logInUser: (data) ->
        @data.sending = true
        @change()
        recorder.emit('log in user')
        ajax({
            method: 'POST'
            url: '/s/sessions'
            data: data
            done: (response) =>
                @data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('log in user success')
                # Hard redirect to get the HTTP_ONLY cookie
                window.location = '/my_sets'
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('log in user failure', errors)
            always: =>
                @data.sending = false
                @change()
        })

    logOutUser: ->
        @data.sending = true
        @change()
        recorder.emit('log out user')
        ajax({
            method: 'DELETE'
            url: '/s/sessions'
            done: =>
                @data.currentUserID = null
                cookie.unset('currentUserID')
                window.location = '/'
                # Hard redirect to delete the HTTP_ONLY cookie
                recorder.emit('log out user success')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('log out user failure', errors)
            always: =>
                @data.sending = false
                @change()
        })

    getUserPasswordToken: (data) ->
        @data.sending = true
        @change()
        recorder.emit('get password token')
        ajax({
            method: 'POST'
            url: '/s/password_tokens'
            data: data
            done: (response) =>
                @data.passwordPageState = 'inbox'
                recorder.emit('get password token success')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('get password token failure', errors)
            always: =>
                @data.sending = false
                @change()
        })

    createUserPassword: (data) ->
        @data.sending = true
        @change()
        recorder.emit('create password')
        ajax({
            method: 'POST'
            url: "/s/users/#{data.id}/password"
            data: data
            done: (response) =>
                @data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('create password success')
                # Hard redirect to get the HTTP_ONLY cookie
                window.location = '/my_sets'
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('create password failure', errors)
            always: =>
                @data.sending = false
                @change()
        })
})
