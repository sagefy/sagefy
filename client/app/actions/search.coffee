store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    search: ({q, skip = 0, limit = 10, order}) ->
        @data.searchQuery = q
        @data.searchResults = []  # TODO only if new query...
        ajax({
            method: 'GET'
            url: '/s/search'
            data: {q, skip, limit, order}
            done: (response) =>
                @data.searchResults ?= []
                # TODO@ merge or replace as appropriate
                @data.searchResults = response.hits
                recorder.emit('search', response.hits.length)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on search', errors)
            always: =>
                @change()
        })
})
