const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')

module.exports = tasks.add({
    toggleMenu: () => {
        dispatch({
            type: 'TOGGLE_MENU'
        })
    },

    updateMenuContext: ({card, unit, set}) => {
        dispatch({
            type: 'UPDATE_MENU_CONTEXT',
            card,
            unit,
            set,
        })
    }
})
