module.exports = function route(state = {}, action = { type: '' }) {
    if (action.type === 'SET_ROUTE') {
        return action.route
    }
    return state
}
