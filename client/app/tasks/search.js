const tasks = require('../modules/tasks')
const request = require('../modules/request')
const { getState, dispatch } = require('../modules/store')

module.exports = tasks.add({
    search({ q, kind, skip = 0, limit = 10, order }) {
        if (q !== getState().searchQuery) {
            dispatch({ type: 'RESET_SEARCH' })
        }
        dispatch({
            type: 'SET_SEARCH_QUERY',
            q,
        })
        return request({
            method: 'GET',
            url: '/s/search',
            data: { q, kind, skip, limit, order },
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_SEARCH_RESULTS',
                    message: 'search success',
                    results: response.hits,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'search failure',
                    errors,
                })
            })
    },
})
