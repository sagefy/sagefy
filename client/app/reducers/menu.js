const defaultState = {open: false, context: {}}

module.exports = function menu(state = defaultState, action = {type: ''}) {
    if(action.type !== '') {
        return state
    }
    return state
}
