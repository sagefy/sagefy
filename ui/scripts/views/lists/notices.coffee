View = require('../../framework/view')
NoticeView = require('../components/notice')
template = require('../../templates/lists/notices')
_ = require('../../framework/utilities')

class NoticesView extends View
    template: template
    View: NoticeView
    elements: {
        ul: 'ul'
    }
    className: 'col-6'

    constructor: ->
        super
        @views = []

    render: (data) ->
        super
        for datum in data
            view = new @View(_.extend({parent: this}, @viewOptions or {}))
            @views.push(view)
            @ul.appendChild(view.el)
            view.render(datum)

    mark: (id) ->
        for view in @views
            if view.data.id is id
                view.mark()

    remove: ->
        for view in @views
            delete view.parent
            view.remove()
        super

module.exports = NoticesView
