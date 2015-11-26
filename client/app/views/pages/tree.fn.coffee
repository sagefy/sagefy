radius = 9
distance = 36

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

module.exports = {
    putUnitsInLayers
    orderLayers
    calculatePoints
    findUnit
    findLayer
}
