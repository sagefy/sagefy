const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = function userSets(state = [], action = {type: ''}) {
    if(action.type === 'ADD_USER_SETS') {
        return mergeArraysByKey(
            state,
            action.sets,
            'id'
        )
    }
    return state
}
