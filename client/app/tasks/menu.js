const store = require('../modules/store')
const tasks = require('../modules/tasks')

module.exports = tasks.add({
    toggleMenu: () => {
        store.dispatch({
            type: 'TOGGLE_MENU'
        })
    },

    updateMenuContext: ({card, unit, set}) => {
        store.dispatch({
            type: 'UPDATE_MENU_CONTEXT',
            card,
            unit,
            set,
        })
    }
})
