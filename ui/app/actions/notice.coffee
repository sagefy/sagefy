store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    markNotice: (id) ->
        return ajax({
            method: 'PUT'
            url: "/api/notices/#{id}/read/"
            done: (data) =>
                for index, notice of @data.notices
                    if notice.id is id
                        @data.notices[index] = data.notice
                        break
                recorder.emit('mark notice read', id)
                @change()
        })

    fetchNotices: ->
        # TODO@
        # limit: 20
        # skip: 0
        # "/api/notices/?limit=#{@limit}&skip=#{@skip}"
})
