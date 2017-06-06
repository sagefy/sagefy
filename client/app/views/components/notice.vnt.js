const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .notice'(e, el) {
        if (el.classList.contains('notice--unread')) {
            tasks.markNotice(el.id)
        }
    },
})
