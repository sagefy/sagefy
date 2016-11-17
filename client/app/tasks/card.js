const store = require('../modules/store')
const tasks = require('../modules/tasks')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {mergeArraysByKey, matchesRoute} = require('../modules/auxiliaries')
const errorsReducer = require('../reducers/errors')
const sendingReducer = require('../reducers/sending')
const cardsReducer = require('../reducers/cards')

module.exports = tasks.add({
    getCard: (id) => {
        recorder.emit('get card', id)
        ajax({
            method: 'GET',
            url: `/s/cards/${id}`,
            data: {},
            done: (response) => {
                store.update('cards', cardsReducer, {
                    type: 'GET_CARD_SUCCESS',
                    card: response.card,
                    topics: response.topics,
                    versions: response.versions,
                    card_parameters: response.card_parameters,
                    unit: response.unit,
                    requires: response.requires,
                    required_by: response.required_by,
                    id,
                })
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'get card failure',
                    errors,
                })
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
                tasks.updateMenuContext({card: id})
                recorder.emit('learn card success', id)
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'learn card failure',
                    errors,
                })
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
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'list card versions failure',
                    errors,
                })
            }
        })
    },

    respondToCard: (id, data, goNext = false) => {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
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
                tasks.updateMenuContext({card: false})
                recorder.emit('respond to card success', id)
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'respond to card failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
                if (goNext) {
                    tasks.nextState()
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
            tasks.route(`/cards/${args[0]}/learn`)
        }
        args = matchesRoute(path, '/s/sets/{id}/units')
        if (args) {
            tasks.route(`/sets/${args[0]}/choose_unit`)
        }
        args = matchesRoute(path, '/s/sets/{id}/tree')
        if (args) {
            tasks.route(`/sets/${args[0]}/tree`)
        }
    },

    needAnAnswer: () => {
        recorder.emit('need an answer')
        store.data.cardFeedback = 'Please provide an answer.'
        store.change()
    }
})
