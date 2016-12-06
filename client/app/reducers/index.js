/* eslint-disable global-require */

function combineReducers(reducerMap) {
    const keys = Object.keys(reducerMap)
    return function combinedReducer(prevState = {}, action = {type: ''}) {
        return keys.reduce((newState, key) => {
            newState[key] = reducerMap[key](prevState[key], action)
            return newState
        }, {})
    }
}

// TODO-3 change file names to camelcase to match other files

module.exports = combineReducers({
    cardFeedback: require('./cardFeedback'),
    cardResponse: require('./cardResponse'),
    cardVersions: require('./cardVersions'),
    cards: require('./cards'),
    chooseUnit: require('./chooseUnit'),
    currentTreeUnit: require('./currentTreeUnit'),
    currentUserID: require('./currentUserID'),
    errors: require('./errors'),
    follows: require('./follows'),
    formData: require('./formData'),
    learnCards: require('./learnCards'),
    menu: require('./menu'),
    next: require('./next'),
    notices: require('./notices'),
    passwordPageState: require('./passwordPageState'),
    recommendedSets: require('./recommendedSets'),
    route: require('./route'),
    routeQuery: require('./routeQuery'),
    searchQuery: require('./searchQuery'),
    searchResults: require('./searchResults'),
    sending: require('./sending'),
    setTrees: require('./setTrees'),
    setVersions: require('./setVersions'),
    sets: require('./sets'),
    topicPosts: require('./topicPosts'),
    topics: require('./topics'),
    unitLearned: require('./unitLearned'),
    unitVersions: require('./unitVersions'),
    units: require('./units'),
    users: require('./users'),
    userSets: require('./userSets'),
})
