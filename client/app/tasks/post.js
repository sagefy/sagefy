/* eslint-disable camelcase */
const flattenDeep = require('lodash.flattendeep')
const request = require('../helpers/request')

module.exports = store => {
  const { dispatch, getTasks } = store
  store.addTasks({
    listPostsForTopic(id) {
      return getTasks()
        .listPosts(id)
        .then(response => {
          const userIds = response.posts.map(post => post.user_id)
          const entityVersions = flattenDeep(
            response.posts
              .filter(post => post.kind === 'proposal')
              .map(post => post.entity_versions)
          )
          return Promise.all([
            getTasks()
              .getTopic(id)
              .then(xresponse => {
                const kind = xresponse.topic.entity_kind
                const entityId = xresponse.topic.entity_id
                return getTasks().getEntity(kind, entityId)
              }),
            getTasks().listUsers(userIds, { size: 48 }),
            getTasks().listEntityVersionsByTopic(id, entityVersions),
          ])
        })
    },

    listPosts(id) {
      dispatch({ type: 'LIST_POSTS', id })
      return request({
        method: 'GET',
        url: `/s/topics/${id}/posts`,
        data: {},
        rq: store.requestCookie, // SSR only
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
        rq: store.requestCookie, // SSR only
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
          getTasks().route(`/topics/${topicId}`) // TODO-2 only when in form
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
        rq: store.requestCookie, // SSR only
      })
        .then(response => {
          dispatch({
            type: 'UPDATE_POST_SUCCESS',
            topicId,
            postId: id,
            post: response.post,
          })
          getTasks().route(`/topics/${topicId}`)
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
}
