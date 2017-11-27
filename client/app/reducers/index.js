/* eslint-disable global-require */

function combineReducers(reducerMap) {
  const keys = Object.keys(reducerMap)
  return function combinedReducer(prevState = {}, action = { type: '' }) {
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
  create: require('./create'),
  errors: require('./errors'),
  follows: require('./follows'),
  formData: require('./formData'),
  learnCards: require('./learnCards'),
  menu: require('./menu'),
  next: require('./next'),
  notices: require('./notices'),
  passwordPageState: require('./passwordPageState'),
  recommendedSubjects: require('./recommendedSubjects'),
  route: require('./route'),
  routeQuery: require('./routeQuery'),
  routeTitle: require('./routeTitle'),
  searchQuery: require('./searchQuery'),
  searchResults: require('./searchResults'),
  sending: require('./sending'),
  subjectTrees: require('./subjectTrees'),
  subjectVersions: require('./subjectVersions'),
  subjects: require('./subjects'),
  topicPosts: require('./topicPosts'),
  topicPostVersions: require('./topicPostVersions'),
  topics: require('./topics'),
  unitLearned: require('./unitLearned'),
  unitVersions: require('./unitVersions'),
  units: require('./units'),
  users: require('./users'),
  userAvatars: require('./userAvatars'),
  userSubjects: require('./userSubjects'),
})
