const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')

const request = require('../modules/request')

module.exports = tasks.add({
    createTopic: (data) => {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        recorder.emit('create topic')
        return request({
            method: 'POST',
            url: '/s/topics',
            data: data,
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_TOPIC',
                    message: 'create topic success',
                    topic: response.topic,
                    id: response.topic.id,
                })
                tasks.route(`/topics/${response.topic.id}`)
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'create topic failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    updateTopic: (data) => {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        recorder.emit('update topic')
        return request({
            method: 'PUT',
            url: `/s/topics/${data.topic.id}`,
            data: data,
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_TOPIC',
                    topic: response.topic,
                    id: data.topic.id,
                    message: 'update topic success',
                })
                tasks.route(`/topics/${data.topic.id}`)
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'update topic failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    }
})
