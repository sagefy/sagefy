module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .tree circle'(e, el) {
      if (e) e.preventDefault()
      if (el.classList.contains('selected')) {
        getTasks().selectTreeUnit()
      } else {
        getTasks().selectTreeUnit(el.id)
      }
    },

    'click .tree text'(e) {
      if (e) e.preventDefault()
      getTasks().selectTreeUnit()
    },
  })
}
