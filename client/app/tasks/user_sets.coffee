store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listUserSets: (limit = 50, skip = 0) ->
        userID = @data.currentUserID
        recorder.emit('list user sets')
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
                recorder.emit('list user sets success')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('list user sets failure', errors)
            always: =>
                @change()
        })

    addUserSet: (setID) ->
        userID = @data.currentUserID
        recorder.emit('add user set', setID)
        ajax({
            method: 'POST'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) =>
                @data.userSets.push(response.set)
                recorder.emit('add user set success', setID)
                @tasks.route('/my_sets')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('add user set failure', errors)
            always: =>
                @change()
        })

    chooseSet: (setID) ->
        userID = @data.currentUserID
        recorder.emit('choose set', setID)
        ajax({
            method: 'PUT'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) =>
                @tasks.route("/sets/#{setID}/tree")
                recorder.emit('choose set success', setID)
                recorder.emit('next', response.next)
                @tasks.updateMenuContext({set: setID, unit: false, card: false})
                @data.next = response.next
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('choose set failure', errors)
            always: =>
                @change()
        })

    removeUserSet: ->
        userID = @data.currentUserID
        recorder.emit('remove user set', setID)
        ajax({
            method: 'DELETE'
            url: "/s/users/#{userID}/sets/#{setID}"
            data: {}
            done: (response) ->
                # @data TODO
                recorder.emit('remove user set success', setID)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('remove user set failure', errors)
            always: =>
                @change()
        })
})
