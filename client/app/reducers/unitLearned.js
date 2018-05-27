const clone = require('lodash.clone')

module.exports = function unitLearned(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_UNIT_LEARNED') {
    state = clone(state)
    state[action.unit_id] = action.learned
    return state
  }
  return state
}
