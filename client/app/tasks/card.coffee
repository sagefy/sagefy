store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    getCard: (id) ->
        ajax({
            method: 'GET'
            url: "/s/cards/#{id}"
            data: {}
            done: (response) =>
                @data.cards ?= {}
                card = response.card
                ['topics', 'versions', 'card_parameters'].forEach((r) ->
                    card[r] = response[r]
                )
                card.relationships = [{
                    kind: 'belongs_to'
                    entity: response.unit
                }]
                ['requires', 'required_by'].forEach((r) ->
                    response[r].forEach((e) ->
                        card.relationships.push({
                            kind: r
                            entity: e
                        })
                    )
                )
                @data.cards[id] = card
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
            url: "/s/cards/#{id}/learn"
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
            url: "/s/cards/#{id}/versions"
            data: {}
            done: (response) =>
                @data.cardVersions ?= {}
                @data.cardVersions[id] ?= []
                @data.cardVersions[id] = mergeArraysByKey(
                    @data.cardVersions[id]
                    response.versions
                    'entity_id'
                )
                recorder.emit('list card versions')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list card versions', errors)
            always: =>
                @change()
        })

    respondToCard: (id, data) ->
        @data.sending = true
        @change()

        ajax({
            method: 'POST'
            url: "/s/cards/#{id}/responses"
            data: data
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
