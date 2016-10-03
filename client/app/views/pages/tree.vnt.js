const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .tree circle': (e, el) => {
        if(e) e.preventDefault()
        if (el.classList.contains('selected')) {
            tasks.selectTreeUnit()
        } else {
            tasks.selectTreeUnit(el.id)
        }
    },

    'click .tree text': (e) => {
        if(e) e.preventDefault()
        tasks.selectTreeUnit()
    }
})
