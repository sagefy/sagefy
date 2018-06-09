module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .follow-button'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const [, kind, id] = el.id.match(/^(.*?)_(.*?)$/)
      getTasks().follow({
        entity_id: id,
        entity_kind: kind,
      })
    },
  })
}
