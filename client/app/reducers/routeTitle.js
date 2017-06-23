module.exports = function routeQuery(state = '', action = { type: '' }) {
    if (action.type === 'SET_ROUTE') {
        return action.title
    }
    return state
}
