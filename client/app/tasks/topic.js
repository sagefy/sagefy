const store = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')
const recorder = require('../modules/recorder')
const errorsReducer = require('../reducers/errors')
const sendingReducer = require('../reducers/sending')

module.exports = tasks.add({
    createTopic: (data) => {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        recorder.emit('create topic')
        request({
            method: 'POST',
            url: '/s/topics',
            data: data,
            done: (response) => {
                store.data.topics = store.data.topics || {}
                store.data.topics[response.topic.id] = response.topic
                recorder.emit('create topic success')
                tasks.route(`/topics/${response.topic.id}`)
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'create topic failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            }
        })
    },

    updateTopic: (data) => {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        recorder.emit('update topic')
        request({
            method: 'PUT',
            url: `/s/topics/${data.topic.id}`,
            data: data,
            done: (response) => {
                store.data.topics = store.data.topics || {}
                store.data.topics[data.topic.id] = response.topic
                recorder.emit('update topic success')
                tasks.route(`/topics/${data.topic.id}`)
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'update topic failure',
                    errors,
                })
            },
            always: () => {
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            }
        })
    }
})
