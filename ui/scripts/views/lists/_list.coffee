View = require('../../framework/view')
_ = require('../../framework/utilities')

class ListView extends View
    constructor: ->
        super
        @views = []

    render: (data) ->
        super
        for datum in data
            view = new @View(_.extend({parent: this}, @viewOptions or {}))
            @views.push(view)
            @el.appendChild(view.el)
            view.render(datum)

    remove: ->
        for view in @views
            delete view.parent
            view.remove()
        super

module.exports = ListView
