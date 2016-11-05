module.exports = function cardResponse(state = {}, action = {type: ''}) {
    if(action.type !== '') {
        return state
    }
    return state
}
