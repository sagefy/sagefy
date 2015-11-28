broker = require('../../modules/broker')
actions = require('../../modules/actions')
{closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click #choose-unit .engage': (e, el) ->
        e.preventDefault() if e
        ul = closest(el, document.body, 'ul')
        actions.chooseUnit(ul.id, el.id)
})
