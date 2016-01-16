store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listNotices: (limit = 50, skip = 0) ->
        recorder.emit('list notices')
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
                recorder.emit('list notices success', limit, skip)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('list notices failure', errors)
            always: =>
                @change()
        })

    markNotice: (id, read = true) ->
        recorder.emit('mark notice', id, read)
        ajax({
            method: 'PUT'
            url: "/s/notices/#{id}"
            data: {read}
            done: (response) =>
                for index, notice of @data.notices
                    if notice.id is id
                        @data.notices[index] = response.notice
                        break
                recorder.emit('mark notice success', id, read)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('mark notice failure', errors)
            always: =>
                @change()
        })
})
