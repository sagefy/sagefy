module.exports = (data) ->
    return button(
        {type: 'submit'}
        i(
            {className: "fa fa-#{data.icon}"}
            data.label
        )
    )
