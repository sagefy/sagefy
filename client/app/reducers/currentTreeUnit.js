module.exports = function currentTreeUnit(state = '', action = { type: '' }) {
  if (action.type === 'SET_CURRENT_TREE_UNIT') {
    return action.id
  }
  return state
}
