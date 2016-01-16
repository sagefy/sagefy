broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click #card-learn.choice.answer .continue': (e, el) ->
        e.preventDefault if e
        container = closest(el, '#card-learn')
        response = container
                        .querySelector('[name=choice]:checked')
                        ?.value
        tasks.respondToCard(el.id, {response: response}) if response
        tasks.needAnAnswer() if not response

    'click #card-learn.choice.next-please .continue': (e, el) ->
        e.preventDefault if e
        tasks.nextState()

    'click #card-learn.video .continue': (e, el) ->
        e.preventDefault if e
        tasks.respondToCard(el.id, {}, true)
})
