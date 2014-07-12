Backbone = require('backbone')
template = require('../../templates/components/notifications/index')

class NotificationsView extends Backbone.View
    tagName: 'ul'
    className: 'notifications'

    initialize: (options) ->
        @$region = options.$region
        @collection = options.collection
        @listenTo(@collection, 'sync', @render)
        @collection.fetch({
            read: false
            limit: 20
        })

    render: ->
        @$el.html(template({
            items: @collection.toJSON()
        }))
        @$region.html(@$el)

module.exports = NotificationsView
