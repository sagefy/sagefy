module.exports = function chooseUnit(state = {}, action = { type: '' }) {
  if (action.type === 'SET_CHOOSE_UNIT') {
    return action.chooseUnit
  }
  return state
}
