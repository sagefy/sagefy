module.exports = function errors(state = [], action = { type: '' }) {
    if (action.type === 'SET_ERRORS') {
        return state.errors
    }
    if (action.type === 'RESET_ERRORS') {
        return []
    }
    return state
}
