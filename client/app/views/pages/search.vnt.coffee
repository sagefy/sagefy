broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click #search [type="submit"]': (e, el) ->
        e.preventDefault() if e
        form = closest(el, 'form')
        input = form.querySelector('input')
        tasks.search({q: input.value})

    'click .add-to-my-sets': (e, el) ->
        e.preventDefault() if e
        tasks.addUserSet(el.id)
})
