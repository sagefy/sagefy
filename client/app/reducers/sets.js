const {shallowCopy} = require('../modules/utilities')

module.exports = function sets(state = {}, action = {type: ''}) {
    if(action.type === 'ADD_SET') {
        state = shallowCopy(state)
        state[action.set.entity_id] = action.set
        return state
    }
    return state
}
