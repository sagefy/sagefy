const { shallowCopy } = require('../helpers/utilities')
const { mergeArraysByKey } = require('../helpers/auxiliaries')

module.exports = function topicPosts(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_TOPIC_POSTS') {
    state = shallowCopy(state)
    let posts = state[action.topic_id] || []
    posts = mergeArraysByKey(posts, action.posts, 'id')
    state[action.topic_id] = posts
    return state
  }
  if (action.type === 'UPDATE_POST_SUCCESS') {
    state = shallowCopy(state)
    const posts = state[action.topicId].slice() || []
    const index = posts.findIndex(post => post.id === action.postId)
    posts[index] = action.post
    state[action.topicId] = posts
    return state
  }
  return state
}
