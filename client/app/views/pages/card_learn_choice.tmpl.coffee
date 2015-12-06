{div, ul, li, input, label} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    if data.order is 'random'
        options = fisherYates(data.options).map((o) -> o.value)

    if data.max_options_to_show
        options = options.slice(0, data.max_options_to_show)

    # TODO@ add feedback, state management

    return div(
        {className: 'card-learn-choice'}
        div(
            {className: 'leading'}
            data.body
            ul(
                li(
                    label(
                        input({type: 'radio', value: option})
                        option
                    )
                ) for option in options
            )
        )
    )

fisherYates = (arr) ->
    i = arr.length
    if i is 0 then return arr

    while --i
        j = Math.floor(Math.random() * (i + 1))
        [arr[i], arr[j]] = [arr[j], arr[i]]

    return arr
