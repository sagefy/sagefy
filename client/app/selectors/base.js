function getIsLoggedIn(state) {
  if (!state.checkedSession) {
    return null
  }
  if (!state.currentUserID) {
    return false
  }
  return true
}

module.exports = { getIsLoggedIn }
