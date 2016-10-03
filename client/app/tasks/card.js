const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {mergeArraysByKey, matchesRoute} = require('../modules/auxiliaries')

module.exports = store.add({
    getCard: (id) => {
        recorder.emit('get card', id)
        ajax({
            method: 'GET',
            url: `/s/cards/${id}`,
            data: {},
            done: (response) => {
                store.data.cards = store.data.cards || {}
                const card = response.card
                ;['topics', 'versions', 'card_parameters'].forEach((r) =>
                    card[r] = response[r]
                )
                card.relationships = [{
                    kind: 'belongs_to',
                    entity: response.unit,
                }]
                ;['requires', 'required_by'].forEach((r) =>
                    response[r].forEach((e) =>
                        card.relationships.push({
                            kind: r,
                            entity: e,
                        })
                    )
                )
                store.data.cards[id] = card
                recorder.emit('get card success', id)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('get card failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    getCardForLearn: (id) => {
        delete store.data.cardResponse
        delete store.data.cardFeedback
        recorder.emit('learn card', id)
        ajax({
            method: 'GET',
            url: `/s/cards/${id}/learn`,
            data: {},
            done: (response) => {
                store.data.learnCards = store.data.learnCards || {}
                store.data.learnCards[id] = response.card
                store.tasks.updateMenuContext({card: id})
                recorder.emit('learn card success', id)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('learn card failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    listCardVersions: (id) => {
        recorder.emit('list card versions', id)
        ajax({
            method: 'GET',
            url: `/s/cards/${id}/versions`,
            data: {},
            done: (response) => {
                store.data.cardVersions = store.data.cardVersions || {}
                store.data.cardVersions[id] = store.data.cardVersions[id] || []
                store.data.cardVersions[id] = mergeArraysByKey(
                    store.data.cardVersions[id],
                    response.versions,
                    'entity_id'
                )
                recorder.emit('list card versions success', id)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('list card versions failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    respondToCard: (id, data, goNext = false) => {
        store.data.sending = true
        store.change()
        recorder.emit('respond to card', id)
        ajax({
            method: 'POST',
            url: `/s/cards/${id}/responses`,
            data: data,
            done: (response) => {
                if (response.next) {
                    recorder.emit('next', response.next)
                    store.data.next = response.next
                }
                store.data.cardResponse = response.response
                store.data.unitLearned = store.data.unitLearned || {}
                store.data.unitLearned[response.response.unit_id] =
                    response.response.learned
                store.data.cardFeedback = response.feedback
                store.tasks.updateMenuContext({card: false})
                recorder.emit('respond to card success', id)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('respond to card failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
                if (goNext) {
                    store.tasks.nextState()
                }
            }
        })
    },

    nextState: () => {
        recorder.emit('next state')
        const path = store.data.next.path
        let args
        args = matchesRoute(path, '/s/cards/{id}/learn')
        if (args) {
            store.tasks.route(`/cards/${args[0]}/learn`)
        }
        args = matchesRoute(path, '/s/sets/{id}/units')
        if (args) {
            store.tasks.route(`/sets/${args[0]}/choose_unit`)
        }
        args = matchesRoute(path, '/s/sets/{id}/tree')
        if (args) {
            store.tasks.route(`/sets/${args[0]}/tree`)
        }
    },

    needAnAnswer: () => {
        recorder.emit('need an answer')
        store.data.cardFeedback = 'Please provide an answer.'
        store.change()
    }
})
