module.exports = function userAvatars(state = {}, action = {type: ''}) {
    if(action.type === 'ADD_USER_AVATARS') {
        return Object.assign({}, state, action.avatars)
    }
    return state
}
