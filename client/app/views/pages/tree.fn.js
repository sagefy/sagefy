const radius = 9
const distance = 36

const putUnitsInLayers = (units) => {
    const ids = units.map(unit => unit.entity_id)
    let us = units.map(unit => { // eslint-disable-line
        return {
            id: unit.entity_id,
            requires: unit.require_ids.filter((id) => ids.indexOf(id) > -1),
        }
    })
    const layers = []
    let layer = 0
    while (us.length) {
        Object.keys(us).forEach(i => {
            const u = us[i]
            if (!u.requires.length) {
                layers[layer] = layers[layer] || []
                const unit = units.find(unit => unit.entity_id === u.id)
                layers[layer].push({
                    id: unit.entity_id,
                    requires: unit.require_ids,
                })
            }
        })
        us = us.filter((u) => u.requires.length)
        layers[layer].forEach(u => {
            us.forEach(o => {
                const index = o.requires.indexOf(u.id)
                if (index > -1) {
                    o.requires.splice(index, 1)
                }
            })
        })
        layer++
    }
    return layers
}

const orderLayers = layers => layers
// TODO-2 reorder the layers to make the lines more efficient

const calculatePoints = (layers, nodeWidth) => {
    layers.forEach((layer, i) => {
        layer.forEach((unit, j) => {
            unit.x = distance + radius + j * (distance + radius * 2) +
                     (nodeWidth - layer.length) * (radius * 2 + distance) / 2
            unit.y = i * (distance + radius * 2) + distance + radius
        })
    })
    return layers
}

const findUnit = (layers, id) => {
    for (const layer of layers) {
        for (const unit of layer) {
            if (unit.id === id) { return unit }
        }
    }
}

const findLayer = (layers, id) => {
    let output
    layers.forEach((layer, i) => {
        layer.forEach(unit => {
            if (unit.id === id) {
                output = i
                return
            }
        })
    })
    return output
}

module.exports = {
    putUnitsInLayers,
    orderLayers,
    calculatePoints,
    findUnit,
    findLayer
}
