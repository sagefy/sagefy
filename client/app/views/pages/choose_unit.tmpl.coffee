{div, h1, ul, li, a, h3, p, span, i, div} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div({className: 'spinner'}) unless data.chooseUnit

    return div(
        {id: 'choose-unit', className: 'col-10'}
        h1('Choose a Unit')
        ul(
            {id: data.chooseUnit.set.entity_id, className: 'units'}
            li(
                {className: if index is 0 then 'recommended'}
                a(
                    {
                        id: unit.entity_id
                        className: 'engage ' + if index is 0 \
                                then 'button--accent' \
                                else 'button--good'
                    }
                    'Engage!'
                )
                div(
                    h3(unit.name)
                    span(
                        {className: 'label--accent'}
                        i({className: 'fa fa-star'})
                        ' Recommended'
                    ) if index is 0
                    p(unit.body)
                    # TODO-2 % learned
                )
            ) for unit, index in data.chooseUnit.units.slice(0, 5)
        )
    )
