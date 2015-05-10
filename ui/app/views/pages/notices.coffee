View = require('../../modules/view')
aux = require('../../modules/auxiliaries')

class NoticesPageView extends View
    id: 'notices'

    constructor: ->
        super
        aux.setTitle('Notices')
        @render()
        @on('fetch notices', @showNotices.bind(this))
        @emit('request notices')

        @listenTo(@collection, 'markDone', @markDone.bind(this))
        @listenTo(@view, 'requestMark', @requestMark.bind(this))

    showNotices: (notices) ->
        @render(notices)

    requestMark: (id) ->
        @collection.mark(id)

    markDone: (id) ->
        @view.mark(id)

module.exports = NoticesPageView
