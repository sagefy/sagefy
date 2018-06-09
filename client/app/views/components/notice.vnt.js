module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .notice'(e, el) {
      if (el.classList.contains('notice--unread')) {
        getTasks().markNotice(el.id)
      }
    },
  })
}
