const { div, ul, li, input, label } = require('../../modules/tags')

module.exports = (data, mode) => {
    let { options } = data
    options = options.map((o) => o.value)
    const disabled = mode === 'next-please'

    return [
        div(
            data.body
        ),
        ul(
            { className: 'options card-learn__options' },
            options.map((option, i) => li(
                { className: disabled ? 'disabled' : '' },
                input({
                    type: 'radio',
                    name: 'choice',
                    value: option,
                    id: i,
                    disabled: disabled,
                    key: `${data.id}-${option}`,
                    // The key ensures the input doesn't stay selected
                    // when changing questions
                }),
                label({
                    htmlFor: i,
                    disabled: disabled,
                }, option)
            ))
        ),
    ]
}
