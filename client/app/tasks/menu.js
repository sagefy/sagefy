const store = require('../modules/store')
const recorder = require('../modules/recorder')

store.init(() => {
    store.data.menu = {open: false, context: {}}
})

module.exports = store.add({
    toggleMenu: () => {
        store.data.menu.open = !store.data.menu.open
        recorder.emit('toggle menu',
            store.data.menu.open ? 'open' : 'closed')
        store.change()
    },

    updateMenuContext: ({card, unit, set}) => {
        recorder.emit('update menu context', {card, unit, set})
        store.data.menu.context = store.data.menu.context || {}
        if (card) { store.data.menu.context.card = card }
        if (unit) { store.data.menu.context.unit = unit }
        if (set) { store.data.menu.context.set = set }
        store.change()
    }
})
