const { shallowCopy } = require('../helpers/utilities')

module.exports = function unitLearned(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_UNIT_LEARNED') {
    state = shallowCopy(state)
    state[action.unit_id] = action.learned
    return state
  }
  return state
}
