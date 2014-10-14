PageAdapter = require('./page')
NoticesView = require('../views/lists/notices')
NoticesCollection = require('../collections/notices')

class DashboardAdapter extends PageAdapter
    url: '/dashboard'
    title: 'Dashboard'  # TODO: trans

    render: ->
        super
        @collection = new NoticesCollection()
        @view = new NoticesView({
            id: 'dashboard'
            region: @page
        })
        @listenTo(@collection, 'sync', @showNotices.bind(this))
        @collection.fetch()

    showNotices: ->
        console.log(@collection.models)
        @view.render()

    remove: ->
        @view.remove()
        super

module.exports = DashboardAdapter
