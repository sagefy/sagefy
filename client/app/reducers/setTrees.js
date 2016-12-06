const {shallowCopy} = require('../modules/utilities')

module.exports = function setTree(state = {}, action = {type: ''}) {
    if(action.type === 'ADD_SET_TREE') {
        state = shallowCopy(state)
        state[action.id] = action.tree
        return state
    }
    return state
}
