module.exports = function next(state = {}, action = {type: ''}) {
    if(action.type !== '') {
        return state
    }
    return state
}
