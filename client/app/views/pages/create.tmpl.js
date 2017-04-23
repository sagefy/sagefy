const {div, h1, p, a, ul, li, small} = require('../../modules/tags')
const info = require('../components/entity_info.tmpl')
const icon = require('../components/icon.tmpl')


module.exports = (/* data */) => {
    return div(
        {id: 'create', className: 'page'},
        h1('Create Cards, Units, and Sets'),
        ul(
            {className: 'create__options'},
            li(
                a(
                    { className: 'create__route', href: '/create/set/1' },
                    icon('set'),
                    ' Create a Set'
                ),
                ' Start here. ',
                small(' (You can add existing units and sets to the new set.)')
            ),
            li(
                a(
                    { className: 'create__route', href: '/create/units/1' },
                    icon('unit'),
                    ' Add Units'
                ),
                ' to an existing set.'
            ),
            li(
                a(
                    { className: 'create__route', href: '/create/cards/1' },
                    icon('card'),
                    ' Add Cards'
                ),
                ' to an existing unit.'
            )
        ),
        info(),
        p(
            'Do you want to change an existing card, unit, or set? ',
            a(
                {href: '/search'},
                icon('search'),
                ' Search for it, then click edit.'
            ),
            '.'
        )
    )
}
