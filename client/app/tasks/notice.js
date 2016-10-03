const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('list notices failure', errors)
            },
            always: () => {
                store.change()
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('mark notice failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    }
})
