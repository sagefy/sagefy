const clone = require('lodash.clone')

module.exports = function subjectTree(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_SUBJECT_TREE') {
    state = clone(state)
    state[action.id] = action.tree
    return state
  }
  return state
}
