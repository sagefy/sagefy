{ol, li} = require('../../modules/tags')

module.exports = ({options, state}) ->
    ol(
        {className: 'wizard'}
        li(
            {
                href: '#'
                className:
                    'wizard__li' +
                    (if state is option.name \
                        then ' wizard__li--selected' \
                        else '')
            }
            option.label
        ) for option in options
    )
