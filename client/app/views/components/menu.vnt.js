module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .menu__overlay, .menu__trigger, .menu__item a'(e) {
      if (e) {
        e.preventDefault()
      }
      getTasks().toggleMenu()
    },

    'click [href="#log_out"]'(e) {
      if (e) {
        e.preventDefault()
      }
      getTasks().logOutUser()
    },
  })
}
