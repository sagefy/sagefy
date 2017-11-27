const { div, h1, p, a, ul, li, small } = require('../../modules/tags')
const info = require('../components/entity_info.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = () => {
  return div(
    { id: 'create', className: 'page' },
    h1('Create Cards, Units, and Subjects'),
    ul(
      { className: 'create__options' },
      li(
        a(
          {
            className: 'create__route ',
            href: '/create/subject/create',
          },
          icon('subject'),
          ' Create a Subject'
        ),
        ' Start here. ',
        small(
          ' (You can add existing units and ',
          'subjects to the new subject.)'
        )
      ),
      li(
        a(
          { className: 'create__route', href: '/create/unit/find' },
          icon('unit'),
          ' Add Units'
        ),
        ' to an existing subject.'
      ),
      li(
        a(
          { className: 'create__route', href: '/create/card/find' },
          icon('card'),
          ' Add Cards'
        ),
        ' to an existing unit.'
      )
    ),
    info(),
    p(
      'Do you want to change an existing card, unit, or subject? ',
      a(
        { href: '/search' },
        icon('search'),
        ' Search for it, then click edit'
      ),
      '.'
    )
  )
}
