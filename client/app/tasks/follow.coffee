store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{extend} = require('../modules/utilities')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listFollows: (skip = 0, limit = 50) ->
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
                recorder.emit('list follows')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list follows', errors)
            always: =>
                @change()
        })

    askFollow: (entityID) ->
        ajax({
            method: 'GET'
            url: '/s/follows'
            data: {'entity_id': entityID}
            done: (response) =>
                return if response.follows.length is 0
                follow = response.follows[0]
                @data.follows ?= []
                index = @data.follows.findIndex((f) -> f.entity.id is entityID)
                if index > -1
                    @data.follows[index] = follow
                else
                    @data.follows.push(follow)
                # TODO will this cause a bug with mergeArraysByKey later?
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on ask follow', errors)
            always: =>
                @change()
        })

    follow: (data) ->
        ajax({
            method: 'POST'
            url: '/s/follows'
            data: data
            done: (response) =>
                @data.follows ?= []
                @data.follows.push(response.follow)
                recorder.emit('follow', data.entity.id)
                # TODO will this cause a bug with mergeArraysByKey later?
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
                @data.follows ?= []
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