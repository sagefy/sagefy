store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{extend} = require('../modules/utilities')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listFollows: (skip = 0, limit = 50) ->
        recorder.emit('list follows')
        ajax({
            method: 'GET'
            url: '/s/follows'
            data: {skip, limit, entities: true}
            done: (response) =>
                @data.follows ?= []
                @data.follows = mergeArraysByKey(
                    @data.follows
                    response.follows
                    'id'
                )
                for i, follow of @data.follows
                    extend(follow['entity'], response.entities[i])
                recorder.emit('list follows success')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('list follows failure', errors)
            always: =>
                @change()
        })

    askFollow: (entityID) ->
        recorder.emit('ask follow', entityID)
        ajax({
            method: 'GET'
            url: '/s/follows'
            data: {'entity_id': entityID}
            done: (response) =>
                recorder.emit('ask follow success', entityID)
                return if response.follows.length is 0
                follow = response.follows[0]
                @data.follows ?= []
                index = @data.follows.findIndex((f) -> f.entity.id is entityID)
                if index > -1
                    @data.follows[index] = follow
                else
                    @data.follows.push(follow)
                # TODO-3 will this cause a bug with mergeArraysByKey later?
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('ask follow failure', errors)
            always: =>
                @change()
        })

    follow: (data) ->
        recorder.emit('follow', data.entity.id)
        ajax({
            method: 'POST'
            url: '/s/follows'
            data: data
            done: (response) =>
                @data.follows ?= []
                @data.follows.push(response.follow)
                recorder.emit('follow success', data.entity.id)
                # TODO-3 will this cause a bug with mergeArraysByKey later?
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('follow failure', errors)
            always: =>
                @change()
        })

    unfollow: (id) ->
        recorder.emit('unfollow', id)
        ajax({
            method: 'DELETE'
            url: "/s/follows/#{id}"
            done: (response) =>
                @data.follows ?= []
                i = @data.follows.findIndex((follow) -> follow.id is id)
                @data.follows.splice(i, 1)
                recorder.emit('unfollow success', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('unfollow failure', errors)
            always: =>
                @change()
        })
})
