Collection = require('../framework/collection')

class NoticesCollection extends Collection
    url: '/api/notices/'

    parse: (response) ->
        return response.notices

    mark: (id) ->
        @ajax({
            method: 'PUT'
            url: "/api/notices/#{id}/read/"
            done: =>
                @trigger('markDone', id)
        })

module.exports = NoticesCollection
