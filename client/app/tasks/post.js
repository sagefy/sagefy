/* eslint-disable camelcase */
const { dispatch } = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')
const { flatten } = require('../modules/utilities')

module.exports = tasks.add({
  listPostsForTopic(id) {
    return tasks.listPosts(id).then(response => {
      const userIds = response.posts.map(post => post.user_id)
      const entityVersions = flatten(
        response.posts
          .filter(post => post.kind === 'proposal')
          .map(post => post.entity_versions)
      )
      return Promise.all([
        tasks.getTopic(id).then(xresponse => {
          const kind = xresponse.topic.entity_kind
          const entityId = xresponse.topic.entity_id
          return tasks.getEntity(kind, entityId)
        }),
        tasks.listUsers(userIds, { size: 48 }),
        tasks.listEntityVersionsByTopic(id, entityVersions),
      ])
    })
  },

  listPosts(id) {
    dispatch({ type: 'LIST_POSTS', id })
    return request({
      method: 'GET',
      url: `/s/topics/${id}/posts`,
      data: {},
    })
      .then(response => {
        const { posts } = response
        dispatch({
          type: 'ADD_TOPIC_POSTS',
          message: 'list posts success',
          topic_id: id,
          posts,
        })
        return response
      })
      .catch(errors => {
        dispatch({
          type: 'SET_ERRORS',
          message: 'list posts failure',
          errors,
        })
      })
  },

  createPost(data) {
    dispatch({
      type: 'SET_SENDING_ON',
    })
    const topicId = data.post.topicId || data.post.topic_id
    dispatch({ type: 'CREATE_POST', topicId })
    return request({
      method: 'POST',
      url: `/s/topics/${topicId}/posts`,
      data: data.post,
    })
      .then(response => {
        dispatch({
          type: 'ADD_TOPIC_POSTS',
          message: 'create post success',
          topic_id: topicId,
          posts: [response.post],
        })
        dispatch({
          type: 'SET_SENDING_OFF',
        })
        tasks.route(`/topics/${topicId}`) // TODO-2 only when in form
        return response
      })
      .catch(errors => {
        dispatch({
          type: 'SET_ERRORS',
          message: 'create post failure',
          errors,
        })
        dispatch({
          type: 'SET_SENDING_OFF',
        })
      })
  },

  updatePost(data) {
    dispatch({
      type: 'SET_SENDING_ON',
    })
    const { id } = data.post
    const topicId = data.post.topic_id
    dispatch({ type: 'UPDATE_POST' })
    return request({
      method: 'PUT',
      url: `/s/topics/${topicId}/posts/${id}`,
      data: data.post,
    })
      .then(response => {
        dispatch({
          type: 'UPDATE_POST_SUCCESS',
          topicId,
          postId: id,
          post: response.post,
        })
        tasks.route(`/topics/${topicId}`)
        dispatch({
          type: 'SET_SENDING_OFF',
        })
      })
      .catch(errors => {
        dispatch({
          type: 'SET_ERRORS',
          message: 'update post failure',
          errors,
        })
        dispatch({
          type: 'SET_SENDING_OFF',
        })
      })
  },
})
