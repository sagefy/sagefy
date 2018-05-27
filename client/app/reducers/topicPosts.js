const clone = require('lodash.clone')
const mergeArraysByKey = require('../helpers/merge_arrays_by_key')

module.exports = function topicPosts(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_TOPIC_POSTS') {
    state = clone(state)
    let posts = state[action.topic_id] || []
    posts = mergeArraysByKey(posts, action.posts, 'id')
    state[action.topic_id] = posts
    return state
  }
  if (action.type === 'UPDATE_POST_SUCCESS') {
    state = clone(state)
    const posts = state[action.topicId].slice() || []
    const index = posts.findIndex(post => post.id === action.postId)
    posts[index] = action.post
    state[action.topicId] = posts
    return state
  }
  return state
}
