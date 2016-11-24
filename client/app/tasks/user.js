const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')
const cookie = require('../modules/cookie')
const errorsReducer = require('../reducers/errors')
const sendingReducer = require('../reducers/sending')

const request = require('../modules/request')

// TODO-2 move setting and unsetting of currentUserID back to the server

module.exports = tasks.add({
    createUser(data) {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        store.change()
        recorder.emit('create user')
        request({
            method: 'POST',
            url: '/s/users',
            data: data,
            done: (response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('create user success')
                window.location = '/my_sets'
                // Hard redirect to get the HTTP_ONLY cookie
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'create user failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            }
        })
    },

    updateUser(data) {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        recorder.emit('update user', data.id)
        request({
            method: 'PUT',
            url: `/s/users/${data.id}`,
            data: data,
            done: (response) => {
                store.data.users = store.data.users || {}
                store.data.users[response.user.id] = response.user
                recorder.emit('update user success', response.user.id)
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'update user failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            }
        })
    },

    getCurrentUser() {
        recorder.emit('get current user')
        request({
            method: 'GET',
            url: '/s/users/current',
            done: (response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                store.data.users = store.data.users || {}
                store.data.users[response.user.id] = response.user
                recorder.emit('get current user success')
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'get current user failure',
                    errors,
                })
            }
        })
    },

    getUser(id, opts = {}) {
        recorder.emit('get user', id)
        request({
            method: 'GET',
            url: `/s/users/${id}`,
            data: opts,
            done: (response) => {
                store.data.users = store.data.users || {}
                const user = response.user
                ;['avatar', 'posts', 'sets', 'follows'].forEach((t) => {
                    if (response[t]) { user[t] = response[t] }
                })
                store.data.users[response.user.id] = user
                recorder.emit('get user success', id)
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'get user failure',
                    errors,
                })
            }
        })
    },

    logInUser(data) {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        recorder.emit('log in user')
        request({
            method: 'POST',
            url: '/s/sessions',
            data: data,
            done: (response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('log in user success')
                // Hard redirect to get the HTTP_ONLY cookie
                window.location = '/my_sets'
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'log in user failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            }
        })
    },

    logOutUser() {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        recorder.emit('log out user')
        request({
            method: 'DELETE',
            url: '/s/sessions',
            done: () => {
                store.data.currentUserID = null
                cookie.unset('currentUserID')
                window.location = '/'
                // Hard redirect to delete the HTTP_ONLY cookie
                recorder.emit('log out user success')
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'log out user failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            }
        })
    },

    getUserPasswordToken(data) {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        recorder.emit('get password token')
        request({
            method: 'POST',
            url: '/s/password_tokens',
            data: data,
            done: () => {
                store.data.passwordPageState = 'inbox'
                recorder.emit('get password token success')
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'get password token failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            }
        })
    },

    createUserPassword(data) {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        recorder.emit('create password')
        request({
            method: 'POST',
            url: `/s/users/${data.id}/password`,
            data: data,
            done: (response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('create password success')
                // Hard redirect to get the HTTP_ONLY cookie
                window.location = '/my_sets'
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'create password failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            }
        })
    }
})
