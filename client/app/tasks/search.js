const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    search: ({q, skip = 0, limit = 10, order}) => {
        recorder.emit('search', q)
        if (q !== store.data.searchQuery) {
            store.data.searchResults = []
        }
        store.data.searchQuery = q
        ajax({
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('search failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    }
})
