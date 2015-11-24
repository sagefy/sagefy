{div, h1} = require('../../modules/tags')
{svg, circle, line, text, rect} = require('../../modules/svg_tags')
{copy} = require('../../modules/utilities')

# TODO@ Set Progress (or num learner & quality if contrib)
# TODO@ Click Units:
# TODO@ - Unit name
# TODO@ - Link to unit (not learner)
# TODO@ - Progress, state
# TODO@ Responsive
# TODO Pan
# TODO Zoom

radius = 9
distance = 36
gap = 3

module.exports = (data) ->
    id = data.routeArgs[0]
    treeData = data.setTrees?[id]

    return div({className: 'spinner'}) unless treeData

    layers = orderLayers(putUnitsInLayers(treeData.units))
    nodeHeight = layers.length
    nodeWidth = Math.max.apply(null, layers.map((l) -> l.length))
    width = nodeWidth * radius * 2 + (nodeWidth + 1) * distance
    height = nodeHeight * radius * 2 + (nodeHeight + 1) * distance
    layers = calculatePoints(layers, nodeWidth)

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

            renderLayers(layers)
        )
    )

putUnitsInLayers = (units) ->
    us = ({
        id: unit.entity_id
        requires: copy(unit.require_ids)
    } for unit in units)

    layers = []
    layer = 0

    # TODO@ what if theres a require_id not in the list of units?

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

renderLayers = (layers) ->
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
            nodes.push(unitPoint(unit.x, unit.y))
    return nodes

findUnit = (layers, id) ->
    for layer in layers
        for unit in layer
            if unit.id is id
                return unit

unitPoint = (x, y) ->
    return circle({cx: x, cy: y, r: radius})

unitLine = (x1, y1, x2, y2) ->
    return line({
        x1: x1
        y1: y1 + radius + gap
        x2: x2
        y2: y2 - radius - gap
        'stroke-width': 2
    })
