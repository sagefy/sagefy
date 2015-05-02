PageAdapter = require('./page')
NoticesView = require('../views/lists/notices')
NoticesCollection = require('../collections/notices')

class NoticesAdapter extends PageAdapter
    render: ->
        super
        @collection = new NoticesCollection()
        @view = new NoticesView({
            id: 'notices'
            region: @page
        })
        @listenTo(@collection, 'sync', @showNotices.bind(this))
        @listenTo(@collection, 'markDone', @markDone.bind(this))
        @listenTo(@view, 'requestMark', @requestMark.bind(this))
        @collection.fetch()

    showNotices: ->
        @view.render(@collection.get())

    requestMark: (id) ->
        @collection.mark(id)

    markDone: (id) ->
        @view.mark(id)

    remove: ->
        @view.remove()
        @collection.remove()
        super

module.exports = NoticesAdapter
