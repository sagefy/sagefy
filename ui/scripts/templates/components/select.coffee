c = require('../../modules/content')

module.exports = (data) ->
    if not data.options or data.options.length is 0
        return c('select', 'no_options')

    html = ''

    if data.showOverlay
        html += '<div class="select__selected"></div>'
        # TODO List options that have already been selected
        html += '<div class="select__overlay">'

    if data.showClear
        html += '<a class="clear" href="#">#{c("select", "clear")}</a>'

    if data.showSearch
        html += '<input type="search" name="search">'

    if data.showInline
        html += '<ul class="inline"></ul>'
    else
        html += '<ul></ul>'

    if data.showOverlay
        html += '</div>'  # .select__overlay

    return html
