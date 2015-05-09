View = require('../../modules/view')
aux = require('../../modules/auxiliaries')

class NoticesPageView extends View
    id: 'notices'

    constructor: ->
        super
        aux.setTitle('Notices')
        @render()
        @on('fetched notices', @showNotices.bind(this))
        @emit('requested notices')

        @listenTo(@collection, 'markDone', @markDone.bind(this))
        @listenTo(@view, 'requestMark', @requestMark.bind(this))

    showNotices: (notices) ->
        @render(notices)

    requestMark: (id) ->
        @collection.mark(id)

    markDone: (id) ->
        @view.mark(id)

module.exports = NoticesPageView
