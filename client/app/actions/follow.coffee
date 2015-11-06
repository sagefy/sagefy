store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{extend} = require('../modules/utilities')

module.exports = store.add({
    listFollows: (skip = 0, limit = 50) ->
        ajax({
            method: 'GET'
            url: '/s/follows'
            data: {skip, limit, entities: true}
            done: (response) =>
                @data.follows ?= []
                # TODO@ merge into array by id and created
                @data.follows = response.follows
                for i, follow of @data.follows
                    extend(follow['entity'], response.entities[i])
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
            url: '/s/follows'
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
            url: "/s/follows/#{id}"
            done: (response) =>
                i = @data.follows.findIndex((follow) -> follow.id is id)
                @data.follows.splice(i, 1)
                recorder.emit('unfollow', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on unfollow', errors)
            always: =>
                @change()
        })
})
