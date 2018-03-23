module.exports = function checkedSession(state = false, action = { type: '' }) {
  if (
    action.type === 'SET_CURRENT_USER_ID' ||
    action.type === 'RESET_CURRENT_USER_ID'
  ) {
    return true
  }
  return state
}
