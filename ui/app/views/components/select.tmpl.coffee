###
- name           required, what to send to the API
- count          required, number of options to expect
- url            default: null
- multiple       default: false
- showInline     default: false
- showClear      default: false
- showOverlay    default: false 0-6, true 7+
- showSearch     default: false 0-20 and not url, true 21+ or url
- options:
    either options or url are required .. [{value: '', label: ''}]
###

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
