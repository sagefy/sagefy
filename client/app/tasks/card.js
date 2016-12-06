const store = require('../modules/store')
const tasks = require('../modules/tasks')
const recorder = require('../modules/recorder')
const {matchesRoute} = require('../modules/auxiliaries')
const request = require('../modules/request')

module.exports = tasks.add({
    getCard: (id) => {
        recorder.emit('get card', id)
        return request({
            method: 'GET',
            url: `/s/cards/${id}`,
            data: {},
        })
            .then((response) => {
                store.dispatch({
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
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get card failure',
                    errors,
                })
            })
    },

    getCardForLearn: (id) => {
        store.dispatch({type: 'RESET_CARD_RESPONSE'})
        store.dispatch({type: 'RESET_CARD_FEEDBACK'})
        recorder.emit('learn card', id)
        return request({
            method: 'GET',
            url: `/s/cards/${id}/learn`,
            data: {},
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_LEARN_CARD',
                    message: 'learn card success',
                    card: response.card,
                    id,
                })
                tasks.updateMenuContext({card: id})
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'learn card failure',
                    errors,
                })
            })
    },

    listCardVersions: (id) => {
        recorder.emit('list card versions', id)
        return request({
            method: 'GET',
            url: `/s/cards/${id}/versions`,
            data: {},
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_CARD_VERSIONS',
                    versions: response.versions,
                    message: 'list card versions success',
                    entity_id: id,
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'list card versions failure',
                    errors,
                })
            })
    },

    respondToCard: (id, data, goNext = false) => {
        recorder.emit('respond to card', id)
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        return request({
            method: 'POST',
            url: `/s/cards/${id}/responses`,
            data: data,
        })
            .then((response) => {
                if (response.next) {
                    store.dispatch({
                        type: 'SET_NEXT',
                        next: response.next,
                    })
                }
                store.dispatch({
                    type: 'SET_CARD_RESPONSE',
                    response: response.response
                })
                store.data.unitLearned = store.data.unitLearned || {}
                store.data.unitLearned[response.response.unit_id] =
                    response.response.learned
                store.dispatch({
                    type: 'SET_CARD_FEEDBACK',
                    feedback: response.feedback,
                })
                tasks.updateMenuContext({card: false})
                recorder.emit('respond to card success', id)
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
                if (goNext) {
                    tasks.nextState()
                }
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'respond to card failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
                if (goNext) {
                    tasks.nextState()
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
        store.dispatch({
            type: 'SET_CARD_FEEDBACK',
            feedback: 'Please provide an answer.',
        })
        store.change()
    }
})
