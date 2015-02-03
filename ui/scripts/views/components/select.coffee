View = require('../../framework/view')
util = require('../../framework/utilities')

optTemplate = require('../../templates/components/select_option')

###

Options
-------

- name           required
- field          required, what to send to the API
- options        either options or url are required .. [{value: '', label: ''}]
- url            (default: null)
- showClear      (default: false for 0 or 1, true 2+)
- chooseMultiple (default: false)
- showInline     (default: false)
- showOverlay    (default: false 0-6, true 7+)
- showSearch     (default: false 0-20 and not url, true 21+ or url)

###

class SelectView extends View
    className: 'select'
    tagName: 'span'
    domEvents: {
        'click .clear': 'clearOptions'
        'change input[type="search"]': 'searchOptions'
        'change input[type="radio"], input[type="checkbox"]': 'selectOption'
    }

    constructor: ->
        super
        @options = util.extend({
            title: ''
            slug: aux.slugify(@options.name or '')
            showClear: @options.options?.length > 1
            showOverlay: @options.options?.length > 6
            showSearch: @options.options?.length > 20 or @options.url
        }, @options)

    render: (data) ->
        super
        @el.querySelector('> ul').innerHTML = [@optTemplate({
            chooseMultiple: @options.chooseMultiple
            title: option.label
            name: @options.field
            id: aux.slugify(option.label)
            value: option.value
        }) for option in data.options].join('')

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
            true  # TODO
        else
            true  # TODO
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
