ListView = require('./_list')
NoticeView = require('../components/notice')

class NoticesView extends ListView
    View: NoticeView
    tagName: 'ul'
    className: 'notices col-6'

    mark: (id) ->
        for view in @views
            if view.data.id is id
                view.mark()

module.exports = NoticesView
