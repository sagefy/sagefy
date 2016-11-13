const store = require('../modules/store')
const tasks = require('../modules/tasks')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')
const errorsReducer = require('../reducers/errors')

module.exports = tasks.add({
    listNotices: (limit = 50, skip = 0) => {
        recorder.emit('list notices')
        ajax({
            method: 'GET',
            data: {limit, skip},
            url: '/s/notices',
            done: (response) => {
                store.data.notices = store.data.notices || []
                store.data.notices = mergeArraysByKey(
                    store.data.notices,
                    response.notices,
                    'id'
                )
                recorder.emit('list notices success', limit, skip)
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'list notices failure',
                    errors,
                })
            }
        })
    },

    markNotice: (id, read = true) => {
        recorder.emit('mark notice', id, read)
        ajax({
            method: 'PUT',
            url: `/s/notices/${id}`,
            data: {read},
            done: (response) => {
                store.data.notices.every((notice, index) => {
                    if (notice.id === id) {
                        store.data.notices[index] = response.notice
                    }
                    return notice.id !== id
                })
                recorder.emit('mark notice success', id, read)
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'mark notice failure',
                    errors,
                })
            }
        })
    }
})
