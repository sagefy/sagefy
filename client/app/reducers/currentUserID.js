module.exports = function currentUserID(state = '', action = { type: '' }) {
  if (action.type === 'SET_CURRENT_USER_ID') {
    return action.currentUserID
  }
  if (action.type === 'RESET_CURRENT_USER_ID') {
    return ''
  }
  return state
}
