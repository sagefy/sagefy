store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    listFollows: (skip = 0, limit = 50) ->
        ajax({
            method: 'GET'
            url: '/api/follows'
            data: {skip, limit}
            done: (response) =>
                @data.follows ?= []
                # TODO@ merge into array by id and created
                @data.follows = response.follows
                recorder.emit('list follows')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list follows', errors)
            always: =>
                @change()
        })

    follow: (data) ->
        ajax({
            method: 'POST'
            url: '/api/follows'
            data: data
            done: (response) =>
                # TODO should it be a prepend?
                @data.follows.push(response.follow)
                recorder.emit('follow')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on follow', errors)
            always: =>
                @change()
        })

    unfollow: (id) ->
        ajax({
            method: 'DELETE'
            url: "/api/follows/#{id}"
            done: (response) =>
                # @data  TODO@ filter and find, then splice out
                recorder.emit('unfollow')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on unfollow', errors)
            always: =>
                @change()
        })
})
