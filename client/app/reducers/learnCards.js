const clone = require('lodash.clone')

module.exports = function learnCards(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_LEARN_CARD') {
    state = clone(state)
    state[action.id] = action.card
    return state
  }
  return state
}
