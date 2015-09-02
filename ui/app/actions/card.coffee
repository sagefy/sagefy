store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    getCard: (id) ->
        ajax({
            method: 'GET'
            url: "/api/cards/#{id}"
            data: {}
            done: (response) =>
                @data.cards ?= {}
                @data.cards[id] = response.card
                recorder.emit('get card', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on get card', errors)
            always: =>
                @change()
        })

    getCardForLearn: (id) ->
        ajax({
            method: 'GET'
            url: "/api/cards/#{id}/learn"
            data: {}
            done: (response) =>
                @data.learnCards ?= {}
                @data.learnCards[id] = response.card
                recorder.emit('learn card')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on learn card', errors)
            always: =>
                @change()
        })

    listCardVersions: (id) ->
        ajax({
            method: 'GET'
            url: "/api/cards/#{id}/versions"
            data: {}
            done: (response) =>
                @data.cardVersions ?= {}
                @data.cardVersions[id] ?= []
                @data.cardVersions[id] = response.versions
                # TODO@ merge in array based on id and created
                recorder.emit('list card versions')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list card versions', errors)
            always: =>
                @change()
        })

    respondToCard: (id) ->
        @data.sending = true
        @change()

        ajax({
            method: 'POST'
            url: "/api/cards/#{id}/responses"
            data: {}
            done: (response) =>
                @data.cardResponse = response.response
                recorder.emit('respond to card')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on respond to card', errors)
            always: =>
                @data.sending = false
                @change()
        })
})
