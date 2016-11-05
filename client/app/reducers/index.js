module.exports = function index(state = {}, action = {type: ''}) {
    if(action.type !== '') {
        return state
    }
    return state
}
