{div, h1, strong} = require('../../modules/tags')
{svg, circle, line, text} = require('../../modules/svg_tags')
{copy} = require('../../modules/utilities')


###
TODO@
If learner:
    Set progress
    Nodes colored by status

If contrib:
    Link to set page
###


radius = 9
distance = 36

module.exports = (data) ->
    id = data.routeArgs[0]
    treeData = data.setTrees?[id]

    return div({className: 'spinner'}) unless treeData

    layers = orderLayers(putUnitsInLayers(treeData.units))
    nodeHeight = layers.length
    nodeWidth = Math.max.apply(null, layers.map((l) -> l.length))
    width = nodeWidth * radius * 2 + (nodeWidth + 1) * distance
    width += 12 * (6 * 2 + 5) if data.currentTreeUnit
    height = nodeHeight * radius * 2 + (nodeHeight + 1) * distance
    layers = calculatePoints(layers, nodeWidth)

    currentUnit = treeData.units.find((u) ->
        u.entity_id is data.currentTreeUnit)

    return div(
        {id: 'tree', className: 'col-10'}
        h1("Tree: #{treeData.set.name}")

        svg(
            {
                class: 'tree'
                xmlns: 'http://www.w3.org/2000/svg'
                version: '1.1'
                width: width
                height: height
            }

            renderLayers(layers, currentUnit)
        )
    )

putUnitsInLayers = (units) ->
    ids = (unit.entity_id for unit in units)

    us = ({
        id: unit.entity_id
        requires: unit.require_ids.filter((id) -> id in ids)
    } for unit in units)

    layers = []
    layer = 0

    while us.length
        for i, u of us
            if not u.requires.length
                layers[layer] ?= []
                unit = units.find((unit) -> unit.entity_id is u.id)
                layers[layer].push({
                    id: unit.entity_id
                    requires: unit.require_ids
                })
        us = us.filter((u) -> u.requires.length)
        for u in layers[layer]
            for o in us
                index = o.requires.indexOf(u.id)
                if index > -1
                    o.requires.splice(index, 1)
        layer++

    return layers

orderLayers = (layers) ->
    # TODO reorder the layers to make the lines more efficient
    return layers

calculatePoints = (layers, nodeWidth) ->
    for i, layer of layers
        for j, unit of layer
            unit.x = distance + radius + j * (distance + radius * 2) + \
                     (nodeWidth - layer.length) * (radius * 2 + distance) / 2
            unit.y = i * (distance + radius * 2) + distance + radius
    return layers

renderLayers = (layers, currentUnit) ->
    nodes = []
    # This is done twice to ensure a line never covers over a circle
    for i, layer of layers
        for unit in layer
            for req in unit.requires
                req = findUnit(layers, req)
                nodes.push(unitLine(
                    req.x
                    req.y
                    unit.x
                    unit.y
                ))
    for i, layer of layers
        for unit in layer
            nodes.push(unitPoint(unit, currentUnit?.entity_id))
    if currentUnit
        for i, layer of layers
            for unit in layer
                if unit.id is currentUnit.entity_id
                    nodes.push(text(
                        {
                            class: 'tree__current-unit'
                            x: unit.x + radius + 6
                            y: unit.y + 6
                        }
                        currentUnit.name
                    ))
    return nodes

findUnit = (layers, id) ->
    for layer in layers
        for unit in layer
            if unit.id is id
                return unit

findLayer = (layers, id) ->
    for i, layer of layers
        for unit in layer
            if unit.id is id
                return i

unitPoint = ({id, x, y}, currentTreeUnit) ->
    return circle({
        class: if currentTreeUnit is id then 'selected'
        id: id
        cx: x
        cy: y
        r: radius
    })

unitLine = (x1, y1, x2, y2) ->
    return line({
        x1: x1
        y1: y1
        x2: x2
        y2: y2
        'stroke-width': 2
    })
