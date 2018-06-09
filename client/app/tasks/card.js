const matchesRoute = require('../helpers/matches_route')
const request = require('../helpers/request')

module.exports = store => {
  const { getState, dispatch, getTasks } = store
  return store.addTasks({
    getCard(id) {
      dispatch({ type: 'GET_CARD', id })
      return request({
        method: 'GET',
        url: `/s/cards/${id}`,
        data: {},
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({
            type: 'GET_CARD_SUCCESS',
            card: response.card,
            card_parameters: response.card_parameters,
            unit: response.unit,
            requires: response.requires,
            required_by: response.required_by,
            id,
          })
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'get card failure',
            errors,
          })
        })
    },

    getCardForLearn(id) {
      dispatch({ type: 'RESET_CARD_RESPONSE' })
      dispatch({ type: 'RESET_CARD_FEEDBACK' })
      dispatch({ type: 'GET_LEARN_CARD', id })
      return request({
        method: 'GET',
        url: `/s/cards/${id}/learn`,
        data: {},
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({
            type: 'ADD_LEARN_CARD',
            message: 'learn card success',
            card: response.card,
            id,
          })
          getTasks().updateMenuContext({ card: id })
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'learn card failure',
            errors,
          })
        })
    },

    listCardVersions(id) {
      dispatch({ type: 'LIST_CARD_VERSIONS', id })
      return request({
        method: 'GET',
        url: `/s/cards/${id}/versions`,
        data: {},
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({
            type: 'ADD_CARD_VERSIONS',
            versions: response.versions,
            message: 'list card versions success',
            entity_id: id,
          })
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'list card versions failure',
            errors,
          })
        })
    },

    respondToCard(id, data, goNext = false) {
      dispatch({ type: 'RESPOND_TO_CARD', id })
      dispatch({
        type: 'SET_SENDING_ON',
      })
      return request({
        method: 'POST',
        url: `/s/cards/${id}/responses`,
        data,
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          if (response.next) {
            dispatch({
              type: 'SET_NEXT',
              next: response.next,
            })
          }
          dispatch({
            type: 'SET_CARD_RESPONSE',
            message: 'respond to card success',
            response: response.response,
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
          getTasks().updateMenuContext({ card: false })
          dispatch({
            type: 'SET_SENDING_OFF',
          })
          if (goNext) {
            getTasks().nextState()
          }
        })
        .catch(errors => {
          dispatch({
            type: 'SET_ERRORS',
            message: 'respond to card failure',
            errors,
          })
          dispatch({
            type: 'SET_SENDING_OFF',
          })
          if (goNext) {
            getTasks().nextState()
          }
        })
    },

    nextState() {
      const { path } = getState().next
      let args
      args = matchesRoute(path, '/s/cards/{id}/learn')
      if (args) {
        getTasks().route(`/cards/${args[0]}/learn`)
      }
      args = matchesRoute(path, '/s/subjects/{id}/units')
      if (args) {
        getTasks().route(`/subjects/${args[0]}/choose_unit`)
      }
      args = matchesRoute(path, '/s/subjects/{id}/tree')
      if (args) {
        getTasks().route(`/subjects/${args[0]}/tree`)
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
        cards.forEach(card => {
          request({
            method: 'POST',
            url: '/s/cards/versions',
            data: card,
            rq: store.requestCookie, // SSR only
          })
            .then(response => {
              allResponses.push(response.version)
              count += 1
              if (count === total) {
                resolve({ cards: allResponses })
              }
            })
            .catch(errors => {
              dispatch({
                type: 'SET_ERRORS',
                message: 'create new card version failure',
                errors,
              })
              reject()
            })
        })
      })
    },
  })
}
