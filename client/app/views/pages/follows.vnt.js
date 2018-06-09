/* eslint-disable no-alert */
module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .follows__unfollow-button'(e, el) {
      if (e) {
        e.preventDefault()
      }
      // TODO-2 switch to undo
      if (window.confirm('Unfollow?')) {
        getTasks().unfollow(el.id)
      }
    },
  })
}
