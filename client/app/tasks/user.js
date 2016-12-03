const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')
const cookie = require('../modules/cookie')

const request = require('../modules/request')

// TODO-2 move setting and unsetting of currentUserID back to the server

module.exports = tasks.add({
    createUser(data) {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        store.change()
        recorder.emit('create user')
        return request({
            method: 'POST',
            url: '/s/users',
            data: data,
        })
            .then((response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('create user success')
                window.location = '/my_sets'
                // Hard redirect to get the HTTP_ONLY cookie
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'create user failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    updateUser(data) {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        recorder.emit('update user', data.id)
        return request({
            method: 'PUT',
            url: `/s/users/${data.id}`,
            data: data,
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_USER',
                    user: response.user,
                    message: 'update user success',
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'update user failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    getCurrentUser() {
        recorder.emit('get current user')
        return request({
            method: 'GET',
            url: '/s/users/current',
        })
            .then((response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                store.dispatch({
                    type: 'ADD_USER',
                    user: response.user,
                    message: 'get current user success',
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get current user failure',
                    errors,
                })
            })
    },

    getUser(id, opts = {}) {
        recorder.emit('get user', id)
        return request({
            method: 'GET',
            url: `/s/users/${id}`,
            data: opts,
        })
            .then((response) => {
                const user = response.user
                ;['avatar', 'posts', 'sets', 'follows'].forEach((t) => {
                    if (response[t]) { user[t] = response[t] }
                })
                store.dispatch({
                    type: 'ADD_USER',
                    message: 'get user success',
                    user,
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get user failure',
                    errors,
                })
            })
    },

    logInUser(data) {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        recorder.emit('log in user')
        return request({
            method: 'POST',
            url: '/s/sessions',
            data: data,
        })
            .then((response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('log in user success')
                // Hard redirect to get the HTTP_ONLY cookie
                window.location = '/my_sets'
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'log in user failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    logOutUser() {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        recorder.emit('log out user')
        return request({
            method: 'DELETE',
            url: '/s/sessions',
        })
            .then(() => {
                store.data.currentUserID = null
                cookie.unset('currentUserID')
                window.location = '/'
                // Hard redirect to delete the HTTP_ONLY cookie
                recorder.emit('log out user success')
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'log out user failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    getUserPasswordToken(data) {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        recorder.emit('get password token')
        return request({
            method: 'POST',
            url: '/s/password_tokens',
            data: data,
        })
            .then(() => {
                store.data.passwordPageState = 'inbox'
                recorder.emit('get password token success')
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get password token failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    createUserPassword(data) {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        recorder.emit('create password')
        return request({
            method: 'POST',
            url: `/s/users/${data.id}/password`,
            data: data,
        })
            .then((response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('create password success')
                // Hard redirect to get the HTTP_ONLY cookie
                window.location = '/my_sets'
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'create password failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    }
})
