{li, label, input} = require('../../modules/tags')

module.exports = (data) ->
    return li(
        label(
            {
                className: if data.disabled then 'disabled' else ''
            }
            input({
                type: if data.multiple then 'checkbox' else 'radio'
                value: data.value or ''
                name: data.name
                checked: data.checked
                disabled: data.disabled or false
            })
            ' '
            data.label
        )
    )
