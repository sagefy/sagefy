const { shallowCopy } = require('../modules/utilities')

module.exports = function subjectTree(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_SUBJECT_TREE') {
    state = shallowCopy(state)
    state[action.id] = action.tree
    return state
  }
  return state
}
