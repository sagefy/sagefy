Store = require('../modules/store')
followSchema = require('../schemas/follow')

class FollowStore extends Store
    limit: 20

    constructor: ->
        super
        @skip = 0
        @on('fetched follows', @increment.bind(this))

    url: ->
        return "/api/follows/?limit=#{@limit}&skip=#{@skip}"

    parse: (response) ->
        return response.follows

    increment: ->
        @skip += @limit

module.exports = FollowStore
