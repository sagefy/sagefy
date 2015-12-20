{button, i} = require('../../modules/tags')

module.exports = (data) ->
    return button(
        {
            type: 'submit'
            disabled: data.disabled
            id: data.id
        }
        i({className: "fa fa-#{data.icon}"})
        ' '
        data.label
    )
