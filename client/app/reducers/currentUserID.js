const cookie = require('../modules/cookie')

module.exports = function currentUserID(state = '', action = {type: ''}) {
    if(action.type === 'SET_CURRENT_USER_ID') {
        // TODO-2 I know this is horrible. This should be a listener.
        if (action.currentUserID) {
            cookie.set('currentUserID', action.currentUserID)
        } else {
            cookie.unset('currentUserID')
        }
        return action.currentUserID
    }
    if(action.type === 'RESET_CURRENT_USER_ID') {
        cookie.unset('currentUserID')
        return ''
    }
    return state
}
