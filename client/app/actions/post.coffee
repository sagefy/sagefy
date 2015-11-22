store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    listPosts: (id) ->
        ajax({
            method: 'GET'
            url: "/s/topics/#{id}/posts"
            data: {}
            done: (response) =>
                @data.topics ?= {}
                @data.topics[id] = response.topic

                @data.topicPosts ?= {}
                @data.topicPosts[id] ?= []
                posts = response.posts
                for post in posts
                    user = response.users[post.user_id]
                    post.user_name = user.name
                    post.user_avatar = user.avatar
                @data.topicPosts[id] = posts

                if 'card' of response
                    @data.cards ?= {}
                    @data.cards[response.card.entity_id] = response.card

                else if 'unit' of response
                    @data.units ?= {}
                    @data.units[response.unit.entity_id] = response.unit

                else if 'set' of response
                    @data.sets ?= {}
                    @data.sets[response.set.entity_id] = response.set

                # TODO merge based on id and created  x topic
                recorder.emit('list posts', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list posts', errors)
            always: =>
                @change()
        })

    createPost: (data) ->
        ajax({
            method: 'POST'
            url: "/s/topics/#{data.topic_id}/posts"
            data: data
            done: (response) =>
                @data.posts.push(response.post)   # TODO x topic
                recorder.emit('create post')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on create post', errors)
            always: =>
                @change()
        })

    updatePost: (data) ->
        ajax({
            method: 'PUT'
            url: "/s/topics/#{data.topic_id}/posts/#{data.id}"
            data: data
            done: (response) =>
                # @data.posts TODO findIndex and update   x topic
                @data.posts.push(response.post)
                recorder.emit('update post')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on update post', errors)
            always: =>
                @change()
        })
})
