const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const cookie = require('../modules/cookie')

// TODO-2 move setting and unsetting of currentUserID back to the server

module.exports = store.add({
    createUser: (data) => {
        store.data.sending = true
        store.change()
        recorder.emit('create user')
        ajax({
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
                store.data.errors = errors
                recorder.emit('error on create user', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    },

    updateUser: (data) => {
        store.data.sending = true
        store.change()
        recorder.emit('update user', data.id)
        ajax({
            method: 'PUT',
            url: `/s/users/${data.id}`,
            data: data,
            done: (response) => {
                store.data.users = store.data.users || {}
                store.data.users[response.user.id] = response.user
                recorder.emit('update user success', response.user.id)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('update user failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    },

    getCurrentUser: () => {
        recorder.emit('get current user')
        ajax({
            method: 'GET',
            url: '/s/users/current',
            done: (response) => {
                store.data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                store.data.users = store.data.users || {}
                store.data.users[response.user.id] = response.user
                recorder.emit('get current user success')
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('get current user failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    getUser: (id, opts = {}) => {
        recorder.emit('get user', id)
        ajax({
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('get user failure', id, errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    logInUser: (data) => {
        store.data.sending = true
        store.change()
        recorder.emit('log in user')
        ajax({
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
                store.data.errors = errors
                recorder.emit('log in user failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    },

    logOutUser: () => {
        store.data.sending = true
        store.change()
        recorder.emit('log out user')
        ajax({
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
                store.data.errors = errors
                recorder.emit('log out user failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    },

    getUserPasswordToken: (data) => {
        store.data.sending = true
        store.change()
        recorder.emit('get password token')
        ajax({
            method: 'POST',
            url: '/s/password_tokens',
            data: data,
            done: () => {
                store.data.passwordPageState = 'inbox'
                recorder.emit('get password token success')
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('get password token failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    },

    createUserPassword: (data) => {
        store.data.sending = true
        store.change()
        recorder.emit('create password')
        ajax({
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
                store.data.errors = errors
                recorder.emit('create password failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    }
})
