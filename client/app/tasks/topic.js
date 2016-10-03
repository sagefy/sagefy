const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')

module.exports = store.add({
    createTopic: (data) => {
        store.data.sending = true
        store.change()
        recorder.emit('create topic')
        ajax({
            method: 'POST',
            url: '/s/topics',
            data: data,
            done: (response) => {
                store.data.topics = store.data.topics || {}
                store.data.topics[response.topic.id] = response.topic
                recorder.emit('create topic success')
                store.tasks.route(`/topics/${response.topic.id}`)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('create topic failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    },

    updateTopic: (data) => {
        store.data.sending = true
        store.change()
        recorder.emit('update topic')
        ajax({
            method: 'PUT',
            url: `/s/topics/${data.topic.id}`,
            data: data,
            done: (response) => {
                store.data.topics = store.data.topics || {}
                store.data.topics[data.topic.id] = response.topic
                recorder.emit('update topic success')
                store.tasks.route(`/topics/${data.topic.id}`)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('update topic failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    }
})
