Store = require('../modules/store')

class SearchStore extends Store
    limit: 20

    constructor: ->
        super
        @skip = 0
        @on('fetched results', @increment.bind(this))

    url: ->
        return "/api/search/?limit=#{@limit}&skip=#{@skip}"

    parse: (response) ->
        return response.results

    increment: ->
        @skip += @limit

module.exports = SearchStore
