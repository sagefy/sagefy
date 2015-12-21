###
- name           required, what to send to the API
- count          required, number of options to expect
- url            default: null
- multiple       default: false
- inline         default: false
- showClear      default: false
- showOverlay    default: false 0-6, true 7+
- showSearch     default: false 0-20 and not url, true 21+ or url
- options:
    either options or url are required .. [{value: '', label: ''}]
###

c = require('../../modules/content').get

{div, a, i, ul} = require('../../modules/tags')
{isOneOf} = require('../../modules/validations')
{isArray} = require('../../modules/utilities')

module.exports = (data) ->
    return div(
        {className: 'select'}
        m(data)
    )

m = (data) ->
    if not data.options or data.options.length is 0
        return c('no_options')

    html = []

    html.push(ul(
        {className: 'unstyled' + (if data.inline then ' inline' else '')}
        require('./form_field_select_option.tmpl')({
            name: data.name
            muliple: data.multiple
            value: o.value
            checked: o.value is data.value
            label: o.label
            disabled: o.disabled
        }) for o in data.options
    ))

    # if data.showOverlay
    #     html.push(
    #         div({className: 'select__selected'})
    #         # TODO List options that have already been selected
    #         div({className: 'select__overlay'})
    #     )
    #
    # if data.showClear
    #     html.push(
    #         a(
    #             {className: 'clear', href: '#'}
    #             i({className: 'fa fa-ban'})
    #             c('clear')
    #         )
    #     )
    #
    # if data.showSearch
    #     html.push(
    #         input({type: 'search', name: 'search'})
    #     )

    return html
