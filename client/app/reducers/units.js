const clone = require('lodash.clone')

module.exports = function units(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_UNIT') {
    state = clone(state)
    state[action.unit.entity_id] = action.unit
    return state
  }
  return state
}
