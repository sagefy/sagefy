const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')
const errorsReducer = require('../reducers/errors')

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
                store.data.userSets = store.data.userSets || []
                store.data.userSets = mergeArraysByKey(
                    store.data.userSets,
                    response.sets,
                    'id'
                )
                recorder.emit('list user sets success')
                store.change()
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
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
                store.data.userSets.push(response.set)
                recorder.emit('add user set success', setID)
                tasks.route('/my_sets')
                store.change()
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'add user set failure',
                    errors,
                })
                tasks.route('/my_sets')
                store.change()
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
                store.data.next = response.next
                store.change()
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
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
                store.change()
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'remove user set failure',
                    errors,
                })
            })
    }
})
