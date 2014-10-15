Collection = require('../framework/collection')

class NoticesCollection extends Collection
    limit: 20

    constructor: ->
        super
        @skip = 0
        @on('sync', @increment.bind(this))

    url: ->
        return "/api/notices/?limit=#{@limit}&skip=#{@skip}"

    parse: (response) ->
        return response.notices

    increment: ->
        @skip += @limit

    mark: (id) ->
        @ajax({
            method: 'PUT'
            url: "/api/notices/#{id}/read/"
            done: =>
                @trigger('markDone', id)
        })

module.exports = NoticesCollection
