module.exports = function notices(state = {}, action = {type: ''}) {
    if(action.type !== '') {
        return state
    }
    return state
}
