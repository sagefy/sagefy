{div, ul, li, input, label} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data, mode) ->
    {options} = data
    options = options.map((o) -> o.value)
    disabled = mode is 'next-please'

    return [
        div(
            data.body
        )
        ul(
            {className: 'options card-learn__options'}
            li(
                {className: if disabled then 'disabled' else ''}
                input({
                    type: 'radio'
                    name: 'choice'
                    value: option
                    id: i
                    disabled: disabled
                    key: "#{data.id}-#{option}"
                    # The key ensures the input doesn't stay selected
                    # when changing questions
                })
                label({
                    htmlFor: i
                    disabled: disabled
                }, option)
            ) for option, i in options
        )
    ]
