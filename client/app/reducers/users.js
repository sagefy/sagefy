const clone = require('lodash.clone')

module.exports = function users(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_USER') {
    state = clone(state)
    state[action.user.id] = action.user
    return state
  }
  return state
}
