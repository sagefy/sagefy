const broker = require('../../modules/broker')
// const tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click #topic .follow': (e) => {
        if (e) e.preventDefault()
        // TODO-2 el
    },

    'click #topic .unfollow': (e) => {
        if (e) e.preventDefault()
        // TODO-2 el
    },

    'click #topic .load-more': (e) => {
        if (e) e.preventDefault()
        // TODO-2 el
    }
})
