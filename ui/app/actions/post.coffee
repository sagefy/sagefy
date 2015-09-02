store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    listPosts: (id) ->
        ajax({
            method: 'GET'
            url: "/api/topics/#{id}/posts"
            data: {}
            done: (response) =>
                @data.posts = response.posts
                # TODO merge based on id and created
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
            url: "/api/topics/#{data.topic_id}/posts"
            data: {}
            done: (response) =>
                @data.posts.push(response.post)
                recorder.emit('create post')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on ....', errors)
            always: =>
                @change()
        })

    updatePost: (data) ->
        ajax({
            method: 'PUT'
            url: "/api/topics/#{data.topic_id}/posts/#{data.id}"
            data: {}
            done: (response) =>
                # @data.posts TODO findIndex and update
                recorder.emit('........')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on ....', errors)
            always: =>
                @change()
        })
})
