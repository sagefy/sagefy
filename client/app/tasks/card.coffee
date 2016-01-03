store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey, matchesRoute} = require('../modules/auxiliaries')

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
        delete @data.cardResponse
        delete @data.cardFeedback
        ajax({
            method: 'GET'
            url: "/s/cards/#{id}/learn"
            data: {}
            done: (response) =>
                @data.learnCards ?= {}
                @data.learnCards[id] = response.card
                @tasks.updateMenuContext({card: id})
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

    respondToCard: (id, data, goNext = false) ->
        @data.sending = true
        @change()

        ajax({
            method: 'POST'
            url: "/s/cards/#{id}/responses"
            data: data
            done: (response) =>
                if response.next
                    recorder.emit('next', response.next)
                    @data.next = response.next
                @data.cardResponse = response.response
                @data.unitLearned ?= {}
                @data.unitLearned[response.response.unit_id] =
                    response.response.learned
                @data.cardFeedback = response.feedback
                @tasks.updateMenuContext({card: false})
                recorder.emit('respond to card', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on respond to card', errors)
            always: =>
                @data.sending = false
                @change()
                if goNext
                    @tasks.nextState()
        })

    nextState: () ->
        path = @data.next.path
        if args = matchesRoute(path, '/s/cards/{id}/learn')
            @tasks.route("/cards/#{args[0]}/learn")

    needAnAnswer: () ->
        @data.cardFeedback = 'Please provide an answer.'
        @change()
})
