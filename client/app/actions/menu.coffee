store = require('../modules/store')
recorder = require('../modules/recorder')
{extend} = require('../modules/utilities')
{ucfirst, underscored} = require('../modules/auxiliaries')

store.init(->
    @data.menu = {open: false}
)

module.exports = store.add({
    toggleMenu: ->
        @data.menu.open = not @data.menu.open
        recorder.emit('toggle menu',
            if @data.menu.open then 'open' else 'closed')
        @change()
})
