Collection = require('../framework/collection')

class SearchCollection extends Collection
    limit: 20

    constructor: ->
        super
        @skip = 0
        @on('sync', @increment.bind(this))

    url: ->
        return "/api/search/?limit=#{@limit}&skip=#{@skip}"

    parse: (response) ->
        return response.results

    increment: ->
        @skip += @limit

module.exports = SearchCollection
