View = require('../../modules/view')
util = require('../../modules/utilities')
aux = require('../../modules/auxiliaries')

template = require('./select.tmpl')
optTemplate = require('./select_option.tmpl')

class SelectView extends View
    className: 'select'
    tagName: 'span'
    domEvents: {
        'click .clear': 'clearOptions'
        'change input[type="search"]': 'searchOptions'
        'change input[type="radio"], input[type="checkbox"]': 'updateDisplay'
    }
    template: template

    ###
    - name           required, what to send to the API
    - count          required, number of options to expect
    - url            default: null
    - multiple       default: false
    - showInline     default: false
    - showClear      default: false
    - showOverlay    default: false 0-6, true 7+
    - showSearch     default: false 0-20 and not url, true 21+ or url
    ###
    constructor: ->
        super
        @options = util.extend({
            showOverlay: @options.count > 6
            showSearch: @options.count > 20 or @options.url
        }, @options)

    ###
    - data.options:
        either options or url are required .. [{value: '', label: ''}]
    ###
    render: (data) ->
        @el.innerHTML = @template(util.extend({}, @options, data))
        @renderOptions(data.options)
        @selectElements()
        @delegateEvents()
        return this

    renderOptions: (options) ->
        @el.querySelector('ul').innerHTML = (optTemplate({
            multiple: @options.multiple
            label: option.label
            name: @options.name
            value: option.value
        }) for option in options).join('')

    clearOptions: (e) ->
        e.preventDefault()
        for el in @el.querySelectorAll('input')
            el.checked = false if el.matches([
                '[type="checkbox"]'
                '[type="radio"]'
            ].join(', '))
            el.value = '' if el.matches([
                '[type="text"]'
                '[type="email"]'
                '[type="search"]'
            ].join(', '))

    searchOptions: util.debounce((e) ->
        if @options.url
            true  # TODO@
        else
            true  # TODO@
    , 200)

    updateDisplay: (e) ->
        return if not @options.showOverlay
        els = @el.querySelectorAll([
            'input[type="checkbox"]'
            'input[type="radio"]'
        ].join(', '))
        names = [(el.name or el.value) for el in els].join(', ')
        @el.querySelector('.select__selected').innerHTML = names

module.exports = SelectView
