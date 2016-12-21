const {div, h1, ul, li, a, h3, p, span} = require('../../modules/tags')
// const c = require('../../modules/content').get
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = (data) => {
    if(!Object.keys(data.chooseUnit).length) { return spinner() }
    return div(
        {id: 'choose-unit', className: 'page'},
        h1('Choose a Unit'),
        ul(
            {id: data.chooseUnit.set.entity_id, className: 'units'},
            data.chooseUnit.units.slice(0, 5).map((unit, index) => li(
                {className: index === 0 ? 'recommended' : null},
                a(
                    {
                        id: unit.entity_id,
                        className: 'choose-unit__engage' + (
                            index === 0 ?
                                ' choose-unit__engage--first' :
                                ''
                        )
                    },
                    icon('good'),
                    ' Engage'
                ),
                div(
                    h3(unit.name),
                    index === 0 ? span(
                        {className: 'choose-unit__recommended'},
                        icon('good'),
                        ' Recommended'
                    ) : null,
                    p(unit.body)
                    // TODO-2 % learned
                )
            ))
        )
    )
}
