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
                @data.posts = response.posts
                # TODO merge based on id and created  x topic
                recorder.emit('list posts')
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
