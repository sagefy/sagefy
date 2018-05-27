const { dispatch } = require('../helpers/store')
const tasks = require('../helpers/tasks')

module.exports = tasks.add({
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
