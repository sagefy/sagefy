store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    createTopic: (data) ->
        ajax({
            method: 'POST'
            url: '/s/topics'
            data: data
            done: (response) =>
                @data.topics ?= {}
                @data.topics[response.topic.id] = response.topic
                recorder.emit('create topic')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on create topic', errors)
            always: =>
                @change()
        })

    updateTopic: (data) ->
        ajax({
            method: 'PUT'
            url: "/s/topics/#{data.id}"
            data: data
            done: (response) =>
                @data.topics ?= {}
                @data.topics[data.id] = response.topic
                recorder.emit('update topic')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on update topic', errors)
            always: =>
                @change()
        })

})
