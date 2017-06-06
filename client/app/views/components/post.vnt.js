const broker = require('../../modules/broker')

module.exports = broker.add({
    'click .post .expand'(e) {
        if (e) { e.preventDefault() }
        // TODO-2 el
    },
})
