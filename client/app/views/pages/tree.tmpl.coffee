{div, h1, strong, a, i, p} = require('../../modules/tags')
{svg, circle, line, text} = require('../../modules/svg_tags')
{copy} = require('../../modules/utilities')
{
    putUnitsInLayers
    orderLayers
    calculatePoints
    findUnit
    findLayer
} = require('./tree.fn')
{matchesRoute} = require('../../modules/auxiliaries')

# TODO-2 show the learner their overall set progress as a percent or bar

radius = 9
distance = 36

module.exports = (data) ->
    id = data.routeArgs[0]
    treeData = data.setTrees?[id]

    return div({className: 'spinner'}) unless treeData

    asLearner = data.route.indexOf('as_learner') > -1
    asContrib = not asLearner

    layers = orderLayers(putUnitsInLayers(treeData.units))
    nodeHeight = layers.length
    nodeWidth = Math.max.apply(null, layers.map((l) -> l.length))
    preWidth = width = nodeWidth * radius * 2 + (nodeWidth + 1) * distance
    width += 12 * (6 * 2 + 5) if data.currentTreeUnit
    height = nodeHeight * radius * 2 + (nodeHeight + 1) * distance
    layers = calculatePoints(layers, nodeWidth)

    currentUnit = treeData.units.find((u) ->
        u.entity_id is data.currentTreeUnit)

    if data.next
        [chooseUnitID] = matchesRoute(data.next.path, '/s/sets/{id}/units')
        [cardID] = matchesRoute(data.next.path, '/s/cards/{id}/learn')

    return div(
        {id: 'tree', className: 'col-10'}
        h1("Tree: #{treeData.set.name}")

        p(a(
            {href: "/sets/#{id}"}
            i({className: 'fa fa-chevron-left'})
            ' View set information'
        )) if asContrib

        svg(
            {
                class: 'tree'
                xmlns: 'http://www.w3.org/2000/svg'
                version: '1.1'
                width: width
                height: height
            }

            renderLayers(layers, currentUnit, preWidth, treeData.buckets)
        )

        p(a(
            {
                className: 'button--accent'
                href: "/sets/#{chooseUnitID}/choose_unit"
            }
            'Next '
            i({className: 'fa fa-chevron-right'})
        )) if chooseUnitID

        p(a(
            {className: 'button--accent', href: "/cards/#{cardID}/learn"}
            'Next '
            i({className: 'fa fa-chevron-right'})
        )) if cardID
    )

renderLayers = (layers, currentUnit, preWidth, buckets) ->
    nodes = []
    # TODO-3 break into smaller functions, and there's lots of repetition..
    # This is done twice to ensure a line never covers over a circle
    nodes = nodes.concat(renderLines(layers))
    nodes = nodes.concat(renderPoints(layers, buckets, currentUnit))
    nodes = nodes.concat(renderCurrent(layers, currentUnit, preWidth))
    return nodes

renderLines = (layers) ->
    nodes = []
    for layer in layers
        for unit in layer
            for req in unit.requires
                req = findUnit(layers, req)
                nodes.push(unitLine(
                    req.x
                    req.y
                    unit.x
                    unit.y
                ))
    return nodes

renderPoints = (layers, buckets, currentUnit) ->
    nodes = []
    for layer in layers
        for unit in layer
            for kind, bucket of buckets
                for id in bucket
                    if id is unit.id
                        unit.className = kind
            nodes.push(unitPoint(unit, currentUnit?.entity_id))
    return nodes

renderCurrent = (layers, currentUnit, preWidth) ->
    nodes = []
    if currentUnit
        for layer in layers
            for unit in layer
                if unit.id is currentUnit.entity_id
                    nodes.push(line({
                        class: 'name-line'
                        x1: preWidth
                        y1: unit.y
                        x2: unit.x + radius
                        y2: unit.y
                        'stroke-width': 2
                    }))
                    nodes.push(text(
                        {
                            class: 'tree__current-unit'
                            x: preWidth
                            y: unit.y + 6
                        }
                        currentUnit.name
                    ))
    return nodes

unitPoint = ({id, x, y, className}, currentTreeUnit) ->
    return circle({
        class: className + (if currentTreeUnit is id then ' selected' else '')
        id: id
        cx: x
        cy: y
        r: radius
    })

unitLine = (x1, y1, x2, y2) ->
    return line({
        class: 'unit-require'
        x1: x1
        y1: y1
        x2: x2
        y2: y2
        'stroke-width': 2
    })
