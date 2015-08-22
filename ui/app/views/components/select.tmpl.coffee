c = require('../../modules/content').get

module.exports = (data) ->
    return span(
        {className: 'select'}
        m()
    )

m = ->
    if not data.options or data.options.length is 0
        return c('no_options')

    html = []

    if data.showOverlay
        html.push(
            div({className: 'select__selected'})
            # TODO@ List options that have already been selected
            div({className: 'select__overlay'})
        )

    if data.showClear
        html.push(
            a(
                {className: 'clear', href: '#'}
                i({className: 'fa fa-ban'})
                c('clear')
            )
        )

    if data.showSearch
        html.push(
            input({type: 'search', name: 'search'})
        )

    if data.showInline
        html.push(ul({className: 'inline unstyled'}))
    else
        html.push(ul({className: 'unstyled'}))

    return html
