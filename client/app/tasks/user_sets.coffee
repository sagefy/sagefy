store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listUserSets: (limit = 50, skip = 0) ->
        userID = @data.currentUserID
        ajax({
            method: 'GET'
            url: "/s/users/#{userID}/sets"
            data: {limit, skip}
            done: (response) =>
                @data.userSets ?= []
                @data.userSets = mergeArraysByKey(
                    @data.userSets
                    response.sets
                    'id'
                )
                recorder.emit('list user sets')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list user sets', errors)
            always: =>
                @change()
        })

    addUserSet: (setID) ->
        userID = @data.currentUserID
        ajax({
            method: 'POST'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) =>
                @data.userSets.push(response.set)
                recorder.emit('add user set')
                @tasks.route('/my_sets')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on add user set', errors)
            always: =>
                @change()
        })

    chooseSet: (setID) ->
        userID = @data.currentUserID
        ajax({
            method: 'PUT'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) =>
                @tasks.route("/sets/#{setID}/tree")
                recorder.emit('choose set', setID)
                recorder.emit('next', response.next)
                @data.next = response.next
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on choose set', errors)
            always: =>
                @change()
        })

    removeUserSet: ->
        userID = @data.currentUserID
        ajax({
            method: 'DELETE'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) ->
                # @data TODO
                recorder.emit('remove user set')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on remove user set', errors)
            always: =>
                @change()
        })
})
