store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    createTopic: (data) ->
        @data.sending = true
        @change()
        recorder.emit('create topic')
        ajax({
            method: 'POST'
            url: '/s/topics'
            data: data
            done: (response) =>
                @data.topics ?= {}
                @data.topics[response.topic.id] = response.topic
                recorder.emit('create topic success')
                @tasks.route("/topics/#{response.topic.id}")
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('create topic failure', errors)
            always: =>
                @data.sending = false
                @change()
        })

    updateTopic: (data) ->
        @data.sending = true
        @change()
        recorder.emit('update topic')
        ajax({
            method: 'PUT'
            url: "/s/topics/#{data.topic.id}"
            data: data
            done: (response) =>
                @data.topics ?= {}
                @data.topics[data.topic.id] = response.topic
                recorder.emit('update topic success')
                @tasks.route("/topics/#{data.topic.id}")
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('update topic failure', errors)
            always: =>
                @data.sending = false
                @change()
        })

})
