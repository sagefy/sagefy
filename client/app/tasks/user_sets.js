const store = require('../modules/store')
const tasks = require('../modules/tasks')
const recorder = require('../modules/recorder')
const request = require('../modules/request')

module.exports = tasks.add({
    listUserSets: (limit = 50, skip = 0) => {
        const userID = store.data.currentUserID
        recorder.emit('list user sets')
        return request({
            method: 'GET',
            url: `/s/users/${userID}/sets`,
            data: {limit, skip},
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_USER_SETS',
                    sets: response.sets,
                    message: 'list user sets success',
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'list user sets failure',
                    errors,
                })
            })
    },

    addUserSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('add user set', setID)
        return request({
            method: 'POST',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_USER_SETS',
                    sets: [response.set],
                    message: 'add user set success',
                })
                tasks.route('/my_sets')
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'add user set failure',
                    errors,
                })
                tasks.route('/my_sets')
            })
    },

    chooseSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('choose set', setID)
        return request({
            method: 'PUT',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
        })
            .then((response) => {
                tasks.route(`/sets/${setID}/tree`)
                recorder.emit('choose set success', setID)
                recorder.emit('next', response.next)
                tasks.updateMenuContext({
                    set: setID,
                    unit: false,
                    card: false
                })
                store.dispatch({
                    type: 'SET_NEXT',
                    next: response.next,
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'choose set failure',
                    errors,
                })
            })
    },

    removeUserSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('remove user set', setID)
        return request({
            method: 'DELETE',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
        })
            .then(() => {
                // store.data TODO
                recorder.emit('remove user set success', setID)
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'remove user set failure',
                    errors,
                })
            })
    }
})
