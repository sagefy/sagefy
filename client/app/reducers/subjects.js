const clone = require('lodash.clone')

module.exports = function subjects(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_SUBJECT') {
    state = clone(state)
    state[action.subject.entity_id] = action.subject
    return state
  }
  return state
}
