const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    createTopic: (data) => {
        dispatch({
            type: 'SET_SENDING_ON'
        })
        dispatch({type: 'CREATE_TOPIC'})
        return request({
            method: 'POST',
            url: '/s/topics',
            data: data,
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_TOPIC',
                    message: 'create topic success',
                    topic: response.topic,
                    id: response.topic.id,
                })
                tasks.route(`/topics/${response.topic.id}`)
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'create topic failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    updateTopic: (data) => {
        dispatch({type: 'SET_SENDING_ON'})
        dispatch({type: 'ADD_TOPIC'})
        return request({
            method: 'PUT',
            url: `/s/topics/${data.topic.id}`,
            data: data,
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_TOPIC',
                    topic: response.topic,
                    id: data.topic.id,
                    message: 'update topic success',
                })
                tasks.route(`/topics/${data.topic.id}`)
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'update topic failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    }
})
