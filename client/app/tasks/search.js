const store = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')
const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')
const errorsReducer = require('../reducers/errors')

module.exports = tasks.add({
    search: ({q, skip = 0, limit = 10, order}) => {
        recorder.emit('search', q)
        if (q !== store.data.searchQuery) {
            store.data.searchResults = []
        }
        store.data.searchQuery = q
        request({
            method: 'GET',
            url: '/s/search',
            data: {q, skip, limit, order},
            done: (response) => {
                store.data.searchResults = store.data.searchResults || []
                store.data.searchResults = mergeArraysByKey(
                    store.data.searchResults,
                    response.hits,
                    'id'
                )
                recorder.emit('search success', q, response.hits.length)
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'search failure',
                    errors,
                })
            }
        })
    }
})
