const { dispatch } = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')
const { shallowCopy } = require('../modules/utilities')

module.exports = tasks.add({
  getTopic(id) {
    dispatch({ type: 'GET_TOPIC', id })
    return request({
      method: 'GET',
      url: `/s/topics/${id}`,
    })
      .then(response => {
        dispatch({
          type: 'ADD_TOPIC',
          message: 'create topic success',
          topic: response.topic,
          id: response.topic.id,
        })
        return response
      })
      .catch(errors => {
        dispatch({
          type: 'SET_ERRORS',
          message: 'get topic failure',
          errors,
        })
      })
  },

  listTopics(opts = {}) {
    dispatch({ type: 'LIST_TOPICS', opts })
    return request({
      method: 'GET',
      url: '/s/topics',
      data: opts,
    })
      .then(response => {
        response.topics.forEach(topic => {
          dispatch({
            type: 'ADD_TOPIC',
            message: 'create topic success',
            topic,
            id: topic.id,
          })
        })
        return response
      })
      .catch(errors => {
        dispatch({
          type: 'SET_ERRORS',
          message: 'list topics failure',
          errors,
        })
      })
  },

  createTopicWithPost(data) {
    return tasks.createTopic(data).then(response => {
      const post = shallowCopy(data.post)
      post.topic_id = response.topic.id
      return tasks.createPost({ post })
    })
  },

  createTopic(data) {
    dispatch({
      type: 'SET_SENDING_ON',
    })
    dispatch({ type: 'CREATE_TOPIC' })
    return request({
      method: 'POST',
      url: '/s/topics',
      data: data.topic,
    })
      .then(response => {
        dispatch({
          type: 'ADD_TOPIC',
          message: 'create topic success',
          topic: response.topic,
          id: response.topic.id,
        })
        dispatch({
          type: 'SET_SENDING_OFF',
        })
        return response
      })
      .catch(errors => {
        dispatch({
          type: 'SET_ERRORS',
          message: 'create topic failure',
          errors,
        })
        dispatch({
          type: 'SET_SENDING_OFF',
        })
      })
  },

  updateTopic(data) {
    dispatch({ type: 'SET_SENDING_ON' })
    dispatch({ type: 'UPDATE_TOPIC' })
    return request({
      method: 'PUT',
      url: `/s/topics/${data.topic.id}`,
      data: data.topic,
    })
      .then(response => {
        dispatch({
          type: 'ADD_TOPIC',
          topic: response.topic,
          id: data.topic.id,
          message: 'update topic success',
        })
        tasks.route(`/topics/${data.topic.id}`)
        dispatch({
          type: 'SET_SENDING_OFF',
        })
      })
      .catch(errors => {
        dispatch({
          type: 'SET_ERRORS',
          message: 'update topic failure',
          errors,
        })
        dispatch({
          type: 'SET_SENDING_OFF',
        })
      })
  },
})
