store = require('../modules/store')
recorder = require('../modules/recorder')
{extend} = require('../modules/utilities')
{ucfirst, underscored} = require('../modules/auxiliaries')

store.init(->
    @data.menu = {open: false, context: {}}
)

module.exports = store.add({
    toggleMenu: ->
        @data.menu.open = not @data.menu.open
        recorder.emit('toggle menu',
            if @data.menu.open then 'open' else 'closed')
        @change()

    updateMenuContext: ({card, unit, set}) ->
        @data.menu.context ?= {}
        @data.menu.context.card = card if card?
        @data.menu.context.unit = unit if unit?
        @data.menu.context.set = set if set?
        @change()
})
