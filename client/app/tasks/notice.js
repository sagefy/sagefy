const request = require('../helpers/request')

module.exports = store => {
  const { dispatch } = store
  store.addTasks({
    listNotices(limit = 50, skip = 0) {
      dispatch({ type: 'LIST_NOTICES', limit, skip })
      return request({
        method: 'GET',
        data: { limit, skip },
        url: '/s/notices',
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({
            type: 'LIST_NOTICES_SUCCESS',
            message: 'list notices success',
            limit,
            skip,
            notices: response.notices,
          })
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'list notices failure',
            errors,
          })
        })
    },

    markNotice(id, read = true) {
      dispatch({ type: 'MARK_NOTICE', id, read })
      return request({
        method: 'PUT',
        url: `/s/notices/${id}`,
        data: { read },
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({
            type: 'MARK_NOTICE_SUCCESS',
            message: 'mark notice success',
            id,
            read,
            notice: response.notice,
          })
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'mark notice failure',
            errors,
          })
        })
    },
  })
}
