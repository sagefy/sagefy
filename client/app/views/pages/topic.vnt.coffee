broker = require('../../modules/broker')
tasks = require('../../modules/tasks')

module.exports = broker.add({
    'click #topic .follow': (e, el) ->
        e.preventDefault() if e
        # TODO el

    'click #topic .unfollow': (e, el) ->
        e.preventDefault() if e
        # TODO el

    'click #topic .load-more': (e, el) ->
        e.preventDefault() if e
        # TODO el
})
