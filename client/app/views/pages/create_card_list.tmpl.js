const { div, h1, h3, a, p, hr, ul, li } = require('../../modules/tags')
const { cardWizard } = require('./create_shared.fn')
const icon = require('../components/icon.tmpl')
const previewCardHead = require('../components/preview_card_head.tmpl')

module.exports = function createCardList(data) {
    const { cards } = data.create
    const selectedUnit = data.create.selectedUnit || {}
    const unitName = selectedUnit.name || '???'

    return div(
        { id: 'create', className: 'page create--card-list' },
        h1('Add Cards to Unit'),
        cardWizard('list'),
        h3(`The following cards will be added to ${unitName}`),
        p('We won\'t save the new cards until you "Submit These Cards".'),
        // TODO List of existing units (if any)

        cards && cards.length
            ? ul(
                  { className: 'create--card-list__cards' },
                  cards.map((card, index) =>
                      li(
                          a(
                              {
                                  dataset: { index },
                                  href: '#',
                                  className: 'create--card-list__remove',
                              },
                              icon('remove'),
                              ' Remove'
                          ),
                          previewCardHead({
                              name: card.name,
                              kind: card.kind,
                          })
                      )
                  )
              )
            : p('No cards added yet.'),
        a(
            {
                className: 'create--card-list__create',
                href: '/create/card/create',
            },
            icon('create'),
            ' Create a New Card'
        ),
        hr(),
        a(
            {
                href: '#',
                className: 'create--card-list__submit',
            },
            icon('create'),
            ' Submit These Cards'
        ),
        a(
            {
                href: '/create',
                className: 'create__home',
            },
            icon('back'),
            ' Return to Create Overview'
        )
    )
}
