{div, ul, li, input, label} = require('../../modules/tags')
c = require('../../modules/content').get

# TODO-1 why is this preselecting an option?

module.exports = (data, mode) ->
    {options} = data
    options = options.map((o) -> o.value)

    if data.order is 'random'
        options = fisherYates(options)

    if data.max_options_to_show
        options = options.slice(0, data.max_options_to_show)

    disabled = mode is 'next-please'

    return [
        div(
            {className: 'leading'}
            data.body
        )
        ul(
            {className: 'options unstyled'}
            li(
                {className: if disabled then 'disabled' else ''}
                input({
                    type: 'radio'
                    name: 'choice'
                    value: option
                    id: i
                    disabled: disabled
                })
                label({
                    htmlFor: i
                    disabled: disabled
                }, option)
            ) for option, i in options
        )
    ]

fisherYates = (arr) ->
    i = arr.length
    if i is 0 then return arr

    while --i
        j = Math.floor(Math.random() * (i + 1))
        [arr[i], arr[j]] = [arr[j], arr[i]]

    return arr
