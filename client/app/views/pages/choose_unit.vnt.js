const closest = require('../../helpers/closest')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .choose-unit__engage'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const ul = closest(el, 'ul')
      getTasks().chooseUnit(ul.id, el.id)
    },
  })
}
