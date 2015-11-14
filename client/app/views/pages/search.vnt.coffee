broker = require('../../modules/broker')
actions = require('../../modules/actions')
{closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click #search [type="submit"]': (e, el) ->
        e.preventDefault() if e
        form = closest(el, document.body, 'form')
        input = form.querySelector('input')
        actions.search({q: input.value})

    'click .add-to-my-sets': (e, el) ->
        e.preventDefault() if e
        actions.addUserSet(el.id)
})
