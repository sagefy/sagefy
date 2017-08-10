const { mergeArraysByKey } = require('../modules/auxiliaries')

module.exports = function userSubjects(state = [], action = { type: '' }) {
    if (action.type === 'ADD_USER_SUBJECTS') {
        return mergeArraysByKey(state, action.subjects, 'id')
    }
    return state
}
