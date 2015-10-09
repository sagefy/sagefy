store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    search: ({q, skip, limit, order}) ->
        ajax({
            method: 'GET'
            url: '/s/search'
            data: {q, skip, limit, order}
            done: (response) =>
                @data.search ?= []
                # TODO@ merge or replace as appropriate
                @data.search = response.search
                recorder.emit('search')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on search', errors)
            always: =>
                @change()
        })
})
