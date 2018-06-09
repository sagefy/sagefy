module.exports = store => {
  const { dispatch } = store
  store.addTasks({
    toggleMenu() {
      dispatch({
        type: 'TOGGLE_MENU',
      })
    },

    updateMenuContext({ card, unit, subject }) {
      dispatch({
        type: 'UPDATE_MENU_CONTEXT',
        card,
        unit,
        subject,
      })
    },
  })
}
