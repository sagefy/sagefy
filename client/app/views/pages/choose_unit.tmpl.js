const { div, h1, ul, li, a, h3, span, hgroup } = require('../../modules/tags')
// const c = require('../../modules/content').get
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const previewUnitHead = require('../components/preview_unit_head.tmpl')

module.exports = (data) => {
  if (!Object.keys(data.chooseUnit).length) {
    return spinner()
  }
  return div(
    { id: 'choose-unit', className: 'page' },
    Object.keys(data.unitLearned).length
      ? hgroup(
          h1('Choose a Unit'),
          h3(
            icon('good'),
            ' You just finished a unit! Pick the next one to learn:'
          )
        )
      : h1('Choose a Unit'),
    ul(
      { id: data.chooseUnit.subject.entity_id, className: 'units' },
      data.chooseUnit.units.slice(0, 5).map((unit, index) =>
        li(
          { className: index === 0 ? 'recommended' : null },
          a(
            {
              id: unit.entity_id,
              className: `choose-unit__engage${index === 0
                ? ' choose-unit__engage--first'
                : ''}`,
            },
            'Engage ',
            icon('next')
          ),
          div(
            index === 0
              ? span(
                  { className: 'choose-unit__recommended' },
                  icon('learn'),
                  ' Recommended'
                )
              : null,
            previewUnitHead({
              name: unit.name,
              body: unit.body,
            })
            // TODO-2 % learned
          )
        )
      )
    )
  )
}
