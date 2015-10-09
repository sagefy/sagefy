store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    listUserSets: (limit = 50, skip = 0) ->
        user_id = @data.currentUserID
        ajax({
            method: 'GET'
            url: "/s/users/#{user_id}/sets"
            data: {limit, skip}
            done: (response) =>
                # TODO merge based on ...?
                @data.userSets = response.sets
                recorder.emit('list user sets')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list user sets', errors)
            always: =>
                @change()
        })

    addUserSet: ->
        ajax({
            method: 'POST'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) =>
                @data.userSets.push(response.set)
                recorder.emit('add user set')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on add user set', errors)
            always: =>
                @change()
        })

    chooseSet: ->
        ajax({
            method: 'PUT'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) =>
                # @data  TODO
                recorder.emit('choose set')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on choose set', errors)
            always: =>
                @change()
        })

    removeUserSet: ->
        ajax({
            method: 'DELETE'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) =>
                # @data TODO
                recorder.emit('remove user set')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on remove user set', errors)
            always: =>
                @change()
        })
})
