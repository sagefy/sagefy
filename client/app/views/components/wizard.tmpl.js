const { ol, li } = require('../../modules/tags')

module.exports = ({ options, state }) =>
    ol(
        { className: 'wizard' },
        options.map(option => li(
            {
                href: '#',
                className:
                    `wizard__li${
                    state === option.name ?
                        ' wizard__li--selected' :
                        ''}`,
            },
            option.label
        ))
    )
