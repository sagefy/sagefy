const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')

const request = require('../modules/request')

module.exports = tasks.add({
    listNotices: (limit = 50, skip = 0) => {
        recorder.emit('list notices')
        return request({
            method: 'GET',
            data: {limit, skip},
            url: '/s/notices',
        })
            .then((response) => {
                store.dispatch({
                    type: 'LIST_NOTICES_SUCCESS',
                    message: 'list notices success',
                    limit,
                    skip,
                    notices: response.notices
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'list notices failure',
                    errors,
                })
            })
    },

    markNotice: (id, read = true) => {
        recorder.emit('mark notice', id, read)
        return request({
            method: 'PUT',
            url: `/s/notices/${id}`,
            data: {read},
        })
            .then((response) => {
                store.dispatch({
                    type: 'MARK_NOTICE_SUCCESS',
                    message: 'mark notice success',
                    id,
                    read,
                    notice: response.notice
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'mark notice failure',
                    errors,
                })
            })
    }
})
