store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

store.init(-> @data.menu or= {})

module.exports = store.add({
    toggleMenu: ->
        @data.menu.open = not @data.menu.open
        recorder.emit('toggle menu',
            if @data.menu.open then 'open' else 'closed')
        @change()
})
