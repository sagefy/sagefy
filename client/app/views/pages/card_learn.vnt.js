const closest = require('../../helpers/closest')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click #card-learn.choice-kind.answer .continue'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const container = closest(el, '#card-learn')
      const checked = container.querySelector('[name=choice]:checked')
      const response = checked && checked.value
      if (response) {
        getTasks().respondToCard(el.id, { response })
      } else {
        getTasks().needAnAnswer()
      }
    },

    'click #card-learn.choice-kind.next-please .continue'(e) {
      if (e) {
        e.preventDefault()
      }
      getTasks().nextState()
    },

    'click #card-learn.video-kind .continue'(e, el) {
      if (e) {
        e.preventDefault()
      }
      getTasks().respondToCard(el.id, {}, true)
    },

    'click #card-learn.page-kind .continue'(e, el) {
      if (e) {
        e.preventDefault()
      }
      getTasks().respondToCard(el.id, {}, true)
    },

    'click #card-learn.unscored_embed-kind .continue'(e, el) {
      if (e) {
        e.preventDefault()
      }
      getTasks().respondToCard(el.id, {}, true)
    },
  })
}
