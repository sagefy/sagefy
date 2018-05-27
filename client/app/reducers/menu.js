const defaultState = { open: false, context: {} }
const cloneDeep = require('lodash.clonedeep')

module.exports = function menu(state = defaultState, action = { type: '' }) {
  if (action.type === 'TOGGLE_MENU') {
    const newState = cloneDeep(state)
    newState.open = !state.open
    return newState
  }
  if (action.type === 'UPDATE_MENU_CONTEXT') {
    const newState = cloneDeep(state)
    if (action.card) {
      newState.context.card = action.card
    }
    if (action.unit) {
      newState.context.unit = action.unit
    }
    if (action.subject) {
      newState.context.subject = action.subject
    }
    return newState
  }
  return state
}
