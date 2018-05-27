const { shallowCopy } = require('../helpers/utilities')

module.exports = function users(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_USER') {
    state = shallowCopy(state)
    state[action.user.id] = action.user
    return state
  }
  return state
}
