module.exports = (store, broker) => {
  broker.add({
    'click .post .expand'(e) {
      if (e) {
        e.preventDefault()
      }
      // TODO-2 el
    },
  })
}
