module.exports = function errors(state = {}, action = {type: ''}) {
    if(action.type !== '') {
        return state
    }
    return state
}
