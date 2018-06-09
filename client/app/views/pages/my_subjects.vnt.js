module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .my-subjects__engage-subject'(e) {
      if (e) {
        e.preventDefault()
      }
      const entityID = e.target.id
      getTasks().chooseSubject(entityID)
    },
  })
}
