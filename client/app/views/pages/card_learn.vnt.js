const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const {closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click #card-learn.choice.answer .continue': (e, el) => {
        if(e) { e.preventDefault() }
        const container = closest(el, '#card-learn')
        const checked = container.querySelector('[name=choice]:checked')
        const response = checked && checked.value
        if (response) {
            tasks.respondToCard(el.id, {response})
        } else {
            tasks.needAnAnswer()
        }
    },

    'click #card-learn.choice.next-please .continue': (e) => {
        if(e) { e.preventDefault() }
        tasks.nextState()
    },

    'click #card-learn.video .continue': (e, el) => {
        if(e) { e.preventDefault() }
        tasks.respondToCard(el.id, {}, true)
    }
})
