module.exports = function recommendedSets(state = [], action = {type: ''}) {
    if(action.type === 'SET_RECOMMENDED_SETS') {
        return action.recommendedSets
    }
    return state
}
