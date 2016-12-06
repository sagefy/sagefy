const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    listNotices: (limit = 50, skip = 0) => {
        dispatch({type: 'LIST_NOTICES', limit, skip})
        return request({
            method: 'GET',
            data: {limit, skip},
            url: '/s/notices',
        })
            .then((response) => {
                dispatch({
                    type: 'LIST_NOTICES_SUCCESS',
                    message: 'list notices success',
                    limit,
                    skip,
                    notices: response.notices
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'list notices failure',
                    errors,
                })
            })
    },

    markNotice: (id, read = true) => {
        dispatch({type: 'MARK_NOTICE', id, read})
        return request({
            method: 'PUT',
            url: `/s/notices/${id}`,
            data: {read},
        })
            .then((response) => {
                dispatch({
                    type: 'MARK_NOTICE_SUCCESS',
                    message: 'mark notice success',
                    id,
                    read,
                    notice: response.notice
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'mark notice failure',
                    errors,
                })
            })
    }
})
