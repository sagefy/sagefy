store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listNotices: (limit = 50, skip = 0) ->
        ajax({
            method: 'GET'
            data: {limit, skip}
            url: '/s/notices'
            done: (response) =>
                @data.notices ?= []
                @data.notices = mergeArraysByKey(
                    @data.notices
                    response.notices
                    'id'
                )
                recorder.emit('list notices', limit, skip)
                @change()
        })

    markNotice: (id, read = true) ->
        ajax({
            method: 'PUT'
            url: "/s/notices/#{id}"
            data: {read}
            done: (response) =>
                for index, notice of @data.notices
                    if notice.id is id
                        @data.notices[index] = response.notice
                        break
                recorder.emit('mark notice', id, read)
                @change()
        })
})
