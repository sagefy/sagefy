broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click .tree circle': (e, el) ->
        e.preventDefault() if e
        if el.classList.contains('selected')
            tasks.selectTreeUnit()
        else
            tasks.selectTreeUnit(el.id)

    'click .tree text': (e, el) ->
        e.preventDefault() if e
        tasks.selectTreeUnit()
})
