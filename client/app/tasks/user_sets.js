const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')
const errorsReducer = require('../reducers/errors')

module.exports = tasks.add({
    listUserSets: (limit = 50, skip = 0) => {
        const userID = store.data.currentUserID
        recorder.emit('list user sets')
        isoRequest({
            method: 'GET',
            url: `/s/users/${userID}/sets`,
            data: {limit, skip},
            done: (response) => {
                store.data.userSets = store.data.userSets || []
                store.data.userSets = mergeArraysByKey(
                    store.data.userSets,
                    response.sets,
                    'id'
                )
                recorder.emit('list user sets success')
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'list user sets failure',
                    errors,
                })
            }
        })
    },

    addUserSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('add user set', setID)
        isoRequest({
            method: 'POST',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
            done: (response) => {
                store.data.userSets.push(response.set)
                recorder.emit('add user set success', setID)
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'add user set failure',
                    errors,
                })
            },
            always: () => {
                tasks.route('/my_sets')
                store.change()
            }
        })
    },

    chooseSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('choose set', setID)
        isoRequest({
            method: 'PUT',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
            done: (response) => {
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
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'choose set failure',
                    errors,
                })
            }
        })
    },

    removeUserSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('remove user set', setID)
        isoRequest({
            method: 'DELETE',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
            done: () => {
                // store.data TODO
                recorder.emit('remove user set success', setID)
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'remove user set failure',
                    errors,
                })
            }
        })
    }
})
