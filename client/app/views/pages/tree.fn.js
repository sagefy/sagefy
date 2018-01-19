const radius = 9
const distance = 36

const putUnitsInLayers = units => {
  const ids = units.map(unit => unit.entity_id)
  let us = units.map(unit => ({
    id: unit.entity_id,
    requires: unit.require_ids.filter(id => ids.indexOf(id) > -1),
  }))
  const layers = []
  let layer = 0
  while (us.length) {
    Object.keys(us).forEach(i => {
      const u = us[i]
      if (!u.requires.length) {
        layers[layer] = layers[layer] || []
        const unit = units.find(xunit => xunit.entity_id === u.id)
        layers[layer].push({
          id: unit.entity_id,
          requires: unit.require_ids,
        })
      }
    })
    us = us.filter(u => u.requires.length)
    layers[layer].forEach(u => {
      us.forEach(o => {
        const index = o.requires.indexOf(u.id)
        if (index > -1) {
          o.requires.splice(index, 1)
        }
      })
    })
    layer += 1
  }
  return layers
}

const orderLayers = layers => layers
// TODO-2 reorder the layers to make the lines more efficient

const calculatePoints = (layers, nodeWidth) => {
  layers.forEach((layer, i) => {
    layer.forEach((unit, j) => {
      unit.x =
        distance +
        radius +
        j * (distance + radius * 2) +
        (nodeWidth - layer.length) * (radius * 2 + distance) / 2
      unit.y = i * (distance + radius * 2) + distance + radius
    })
  })
  return layers
}

const findUnit = (layers, id) => {
  for (let j = 0; j < layers.length; j += 1) {
    for (let k = 0; k < layers[j].length; k += 1) {
      const unit = layers[j][k]
      if (unit.id === id) {
        return unit
      }
    }
  }
  return null
}

const findLayer = (layers, id) => {
  let output
  layers.forEach((layer, i) => {
    layer.forEach(unit => {
      if (unit.id === id) {
        output = i
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
  findLayer,
}
