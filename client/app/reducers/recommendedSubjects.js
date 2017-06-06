module.exports = function recommendedSubjects(state = [], action = { type: '' }) {
    if (action.type === 'SET_RECOMMENDED_SUBJECTS') {
        return action.recommendedSubjects
    }
    return state
}
