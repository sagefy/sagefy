const defaultState = {open: false, context: {}}
const {copy} = require('../modules/utilities')

module.exports = function menu(state = defaultState, action = {type: ''}) {
    if(action.type === 'TOGGLE_MENU') {
        const newState = copy(state)
        newState.open = !state.open
        return newState
    }
    if(action.type === 'UPDATE_MENU_CONTEXT') {
        const newState = copy(state)
        if (action.card) { newState.context.card = action.card }
        if (action.unit) { newState.context.unit = action.unit }
        if (action.set) { newState.context.set = action.set }
        return newState
    }
    return state
}
