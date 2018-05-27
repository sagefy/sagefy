const broker = require('../../helpers/broker')
const tasks = require('../../helpers/tasks')
const { closest } = require('../../helpers/utilities')

module.exports = broker.add({
  'click #card-learn.choice-kind.answer .continue'(e, el) {
    if (e) {
      e.preventDefault()
    }
    const container = closest(el, '#card-learn')
    const checked = container.querySelector('[name=choice]:checked')
    const response = checked && checked.value
    if (response) {
      tasks.respondToCard(el.id, { response })
    } else {
      tasks.needAnAnswer()
    }
  },

  'click #card-learn.choice-kind.next-please .continue'(e) {
    if (e) {
      e.preventDefault()
    }
    tasks.nextState()
  },

  'click #card-learn.video-kind .continue'(e, el) {
    if (e) {
      e.preventDefault()
    }
    tasks.respondToCard(el.id, {}, true)
  },

  'click #card-learn.page-kind .continue'(e, el) {
    if (e) {
      e.preventDefault()
    }
    tasks.respondToCard(el.id, {}, true)
  },

  'click #card-learn.unscored_embed-kind .continue'(e, el) {
    if (e) {
      e.preventDefault()
    }
    tasks.respondToCard(el.id, {}, true)
  },
})
