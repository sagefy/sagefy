View = require('../../framework/view')
template = require('./notice.tmpl')

class NoticeView extends View
    tagName: 'li'
    className: 'notice'
    template: template
    domEvents: {
        click: 'requestMark'
    }

    render: (data) ->
        super
        if not data.read
            @el.classList.add('notice--unread')

    requestMark: ->
        if @el.classList.contains('notice--unread')
            @options.parent.emit('requestMark', @data.id)

    mark: ->
        @el.classList.remove('notice--unread')

module.exports = NoticeView
