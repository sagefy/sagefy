const store = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')
const recorder = require('../modules/recorder')
const errorsReducer = require('../reducers/errors')
const noticesReducer = require('../reducers/notices')

module.exports = tasks.add({
    listNotices: (limit = 50, skip = 0) => {
        recorder.emit('list notices')
        request({
            method: 'GET',
            data: {limit, skip},
            url: '/s/notices',
            done: (response) => {
                store.update('notices', noticesReducer, {
                    type: 'LIST_NOTICES_SUCCESS',
                    message: 'list notices success',
                    limit,
                    skip,
                    notices: response.notices
                })
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
        request({
            method: 'PUT',
            url: `/s/notices/${id}`,
            data: {read},
            done: (response) => {
                store.update('notices', noticesReducer, {
                    type: 'MARK_NOTICE_SUCCESS',
                    message: 'mark notice success',
                    id,
                    read,
                    notice: response.notice
                })
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
