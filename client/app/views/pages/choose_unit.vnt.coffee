broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click #choose-unit .engage': (e, el) ->
        e.preventDefault() if e
        ul = closest(el, 'ul')
        tasks.chooseUnit(ul.id, el.id)
})
