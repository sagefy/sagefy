const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listPosts: (id) => {
        recorder.emit('list posts', id)
        ajax({
            method: 'GET',
            url: `/s/topics/${id}/posts`,
            data: {},
            done: (response) => {
                store.data.topics = store.data.topics || {}
                store.data.topics[id] = response.topic

                store.data.topicPosts = store.data.topicPosts || {}
                store.data.topicPosts[id] = store.data.topicPosts[id] || []

                const posts = response.posts
                posts.forEach(post => {
                    const user = response.users[post.user_id]
                    post.user_name = user.name
                    post.user_avatar = user.avatar
                    const ev = response.entity_versions[post.id]
                    if (ev) {
                        post.ev = ev
                    }
                })

                store.data.topicPosts[id] = store.data.topicPosts[id] || []
                store.data.topicPosts[id] = mergeArraysByKey(
                    store.data.topicPosts[id],
                    posts,
                    'id'
                )

                if ('card' in response) {
                    store.data.cards = store.data.cards ||  {}
                    store.data.cards[response.card.entity_id] = response.card
                } else if ('unit' in response) {
                    store.data.units = store.data.units || {}
                    store.data.units[response.unit.entity_id] = response.unit
                } else if ('set' in response){
                    store.data.sets = store.data.sets || {}
                    store.data.sets[response.set.entity_id] = response.set
                }

                recorder.emit('list posts success', id)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('list posts failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    createPost: (data) => {
        store.data.sending = true
        store.change()
        const {topic_id} = data.post
        recorder.emit('create post')
        ajax({
            method: 'POST',
            url: `/s/topics/${topic_id}/posts`,
            data: data,
            done: (response) => {
                if (store.data.topicPosts && store.data.topicPosts[topic_id]) {
                    store.data.topicPosts[topic_id].push(response.post)
                }
                recorder.emit('create post success')
                store.tasks.route(`/topics/${topic_id}`)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('create post failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    },

    updatePost: (data) => {
        store.data.sending = true
        store.change()
        const {topic_id, id} = data.post
        recorder.emit('update post')
        ajax({
            method: 'PUT',
            url: `/s/topics/${topic_id}/posts/${id}`,
            data: data,
            done: (response) => {
                const topic = store.data.topicPosts &&
                              store.data.topicPosts[topic_id]
                if (topic) {
                    const index = topic.findIndex((post) => post.id === id)
                    topic[index] = response.post
                }
                recorder.emit('update post success')
                store.tasks.route(`/topics/${topic_id}`)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('update post failure', errors)
            },
            always: () => {
                store.data.sending = false
                store.change()
            }
        })
    }
})
