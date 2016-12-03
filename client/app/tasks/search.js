const store = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    search: ({q, skip = 0, limit = 10, order}) => {
        if (q !== store.data.searchQuery) {
            store.dispatch({type: 'RESET_SEARCH_RESULTS'})
        }
        store.dispatch({
            type: 'SET_SEARCH_QUERY',
            q,
        })
        return request({
            method: 'GET',
            url: '/s/search',
            data: {q, skip, limit, order},
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_SEARCH_RESULTS',
                    message: 'search success',
                    results: response.hits
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'search failure',
                    errors,
                })
            })
    }
})
