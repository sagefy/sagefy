store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey} = require('../modules/auxiliaries')

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

                @data.topicPosts[id] ?= []
                @data.topicPosts[id] = mergeArraysByKey(
                    @data.topicPosts[id]
                    posts
                    'id'
                )

                if 'card' of response
                    @data.cards ?= {}
                    @data.cards[response.card.entity_id] = response.card

                else if 'unit' of response
                    @data.units ?= {}
                    @data.units[response.unit.entity_id] = response.unit

                else if 'set' of response
                    @data.sets ?= {}
                    @data.sets[response.set.entity_id] = response.set

                recorder.emit('list posts', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list posts', errors)
            always: =>
                @change()
        })

    createPost: (data) ->
        {topic_id} = data.post
        ajax({
            method: 'POST'
            url: "/s/topics/#{topic_id}/posts"
            data: data
            done: (response) =>
                if @data.topicPosts?[topic_id]
                    @data.topicPosts[topic_id].push(response.post)
                recorder.emit('create post')
                @tasks.route("/topics/#{topic_id}")
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on create post', errors)
            always: =>
                @change()
        })

    updatePost: (data) ->
        {topic_id, id} = data.post
        ajax({
            method: 'PUT'
            url: "/s/topics/#{topic_id}/posts/#{id}"
            data: data
            done: (response) =>
                if topic = @data.topicPosts?[topic_id]
                    index = topic.findIndex((post) -> post.id is id)
                    topic[index] = response.post
                recorder.emit('update post')
                @tasks.route("/topics/#{topic_id}")
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on update post', errors)
            always: =>
                @change()
        })

    changePostKind: (kind) ->
        # TODO maybe this should go into a `pageData` object
        #      that gets cleared on route
        @data.postKind = kind
        @change()

    changeEntityKind: (kind) ->
        # TODO maybe this should go into a `pageData` object
        #      that gets cleared on route
        @data.entityKind = kind
        @change()

    changeCardKind: (kind) ->
        # TODO maybe this should go into a `pageData` object
        #      that gets cleared on route
        @data.cardKind = kind
        @change()
})
