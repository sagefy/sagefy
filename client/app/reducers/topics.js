const clone = require('lodash.clone')

module.exports = function topics(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_TOPIC') {
    state = clone(state)
    state[action.id || action.topic.id] = action.topic
    return state
  }
  return state
}
