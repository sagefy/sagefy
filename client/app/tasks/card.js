const {dispatch, getState} = require('../modules/store')
const tasks = require('../modules/tasks')
const {matchesRoute} = require('../modules/auxiliaries')
const request = require('../modules/request')

module.exports = tasks.add({
    getCard(id) {
        dispatch({type: 'GET_CARD', id})
        return request({
            method: 'GET',
            url: `/s/cards/${id}`,
            data: {},
        })
            .then((response) => {
                dispatch({
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
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get card failure',
                    errors,
                })
            })
    },

    getCardForLearn(id) {
        dispatch({type: 'RESET_CARD_RESPONSE'})
        dispatch({type: 'RESET_CARD_FEEDBACK'})
        dispatch({type: 'GET_LEARN_CARD', id})
        return request({
            method: 'GET',
            url: `/s/cards/${id}/learn`,
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_LEARN_CARD',
                    message: 'learn card success',
                    card: response.card,
                    id,
                })
                tasks.updateMenuContext({card: id})
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'learn card failure',
                    errors,
                })
            })
    },

    listCardVersions(id) {
        dispatch({type: 'LIST_CARD_VERSIONS', id})
        return request({
            method: 'GET',
            url: `/s/cards/${id}/versions`,
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_CARD_VERSIONS',
                    versions: response.versions,
                    message: 'list card versions success',
                    entity_id: id,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'list card versions failure',
                    errors,
                })
            })
    },

    respondToCard(id, data, goNext = false) {
        dispatch({type: 'RESPOND_TO_CARD', id})
        dispatch({
            type: 'SET_SENDING_ON'
        })
        return request({
            method: 'POST',
            url: `/s/cards/${id}/responses`,
            data: data,
        })
            .then((response) => {
                if (response.next) {
                    dispatch({
                        type: 'SET_NEXT',
                        next: response.next,
                    })
                }
                dispatch({
                    type: 'SET_CARD_RESPONSE',
                    message: 'respond to card success',
                    response: response.response
                })
                dispatch({
                    type: 'ADD_UNIT_LEARNED',
                    unit_id: response.response.unit_id,
                    learned: response.response.learned,
                })
                dispatch({
                    type: 'SET_CARD_FEEDBACK',
                    feedback: response.feedback,
                })
                tasks.updateMenuContext({card: false})
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
                if (goNext) {
                    tasks.nextState()
                }
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'respond to card failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
                if (goNext) {
                    tasks.nextState()
                }
            })
    },

    nextState() {
        const path = getState().next.path
        let args
        args = matchesRoute(path, '/s/cards/{id}/learn')
        if (args) {
            tasks.route(`/cards/${args[0]}/learn`)
        }
        args = matchesRoute(path, '/s/subjects/{id}/units')
        if (args) {
            tasks.route(`/subjects/${args[0]}/choose_unit`)
        }
        args = matchesRoute(path, '/s/subjects/{id}/tree')
        if (args) {
            tasks.route(`/subjects/${args[0]}/tree`)
        }
    },

    needAnAnswer() {
        dispatch({
            type: 'SET_CARD_FEEDBACK',
            feedback: 'Please provide an answer.',
        })
    },

    createNewCardVersions(cards) {
        let count = 0
        const total = cards.length
        const allResponses = []
        return new Promise((resolve, reject) => {
            cards.forEach((card) => {
                request({
                    method: 'POST',
                    url: '/s/cards/versions',
                    data: card,
                })
                    .then((response) => {
                        allResponses.push(response.version)
                        count++
                        if(count === total) {
                            resolve({cards: allResponses})
                        }
                    })
                    .catch((errors) => {
                        dispatch({
                            type: 'SET_ERRORS',
                            message: 'create new card version failure',
                            errors,
                        })
                        reject()
                    })
            })
        })
    }
})
