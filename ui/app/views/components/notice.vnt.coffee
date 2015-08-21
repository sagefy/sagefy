broker = require('../../modules/broker')
actions = require('../../modules/store').actions

module.exports = broker.add({
    'click .notice': (e, el) ->
        if el.classList.contains('notice--unread')
            actions.markNotice(el.dataset.id)
})
