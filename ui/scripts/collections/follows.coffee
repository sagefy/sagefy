Collection = require('../framework/collection')

class FollowsCollection extends Collection
    limit: 20

    constructor: ->
        super
        @skip = 0
        @on('sync', @increment.bind(this))

    url: ->
        return "/api/follows/?limit=#{@limit}&skip=#{@skip}"

    parse: (response) ->
        return response.follows

    increment: ->
        @skip += @limit

module.exports = FollowsCollection
