const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .create__route': (e, el) => {
        if(e) e.preventDefault()
        const [,, kind, step] = el.pathname.split('/')
        tasks.resetCreate()
        tasks.updateCreateRoute({kind, step})
    },
})
