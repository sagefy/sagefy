Store = require('../modules/store')
noticeSchema = ('../schemas/notice')

class NoticeStore extends Store
    limit: 20

    constructor: ->
        super
        @skip = 0
        @on('fetch notices', @increment.bind(this))

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
                @emit('mark notice read', id)
        })

module.exports = NoticeStore
