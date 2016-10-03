const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listUserSets: (limit = 50, skip = 0) => {
        const userID = store.data.currentUserID
        recorder.emit('list user sets')
        ajax({
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('list user sets failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    addUserSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('add user set', setID)
        ajax({
            method: 'POST',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
            done: (response) => {
                store.data.userSets.push(response.set)
                recorder.emit('add user set success', setID)
                store.tasks.route('/my_sets')
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('add user set failure', errors)
                store.tasks.route('/my_sets')
            },
            always: () => {
                store.change()
            }
        })
    },

    chooseSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('choose set', setID)
        ajax({
            method: 'PUT',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
            done: (response) => {
                store.tasks.route(`/sets/${setID}/tree`)
                recorder.emit('choose set success', setID)
                recorder.emit('next', response.next)
                store.tasks.updateMenuContext({
                    set: setID,
                    unit: false,
                    card: false
                })
                store.data.next = response.next
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('choose set failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    removeUserSet: (setID) => {
        const userID = store.data.currentUserID
        recorder.emit('remove user set', setID)
        ajax({
            method: 'DELETE',
            url: `/s/users/${userID}/sets/${setID}`,
            data: {},
            done: () => {
                // store.data TODO
                recorder.emit('remove user set success', setID)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('remove user set failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    }
})
