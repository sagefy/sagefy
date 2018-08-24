/*

const { div, h1, a, p } = require('../../helpers/tags')
const { svg, circle, line, text } = require('../../helpers/tags')
const {
  putUnitsInLayers,
  orderLayers,
  calculatePoints,
  findUnit,
} = require('./tree.fn')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

// TODO-2 show the learner their overall subject progress as a percent or bar

const radius = 9
const distance = 36

const unitPoint = ({ id, x, y, className }, currentTreeUnit) =>
  circle({
    className: className + (currentTreeUnit === id ? ' selected' : ''),
    id,
    cx: x,
    cy: y,
    r: radius,
  })

const unitLine = ({ x1, y1, x2, y2 }) =>
  line({
    className: 'unit-require',
    x1,
    y1,
    x2,
    y2,
    'stroke-width': 2,
  })

const renderLines = layers => {
  const nodes = []
  layers.forEach(layer => {
    layer.forEach(unit => {
      unit.requires.forEach(req => {
        req = findUnit(layers, req)
        if (req) {
          nodes.push(
            unitLine({
              x1: req.x,
              y1: req.y,
              x2: unit.x,
              y2: unit.y,
            })
          )
        }
      })
    })
  })
  return nodes
}

const renderPoints = (layers, buckets, currentUnit) => {
  const nodes = []
  layers.forEach(layer => {
    layer.forEach(unit => {
      Object.keys(buckets).forEach(kind => {
        const bucket = buckets[kind]
        bucket.forEach(id => {
          if (id === unit.id) {
            unit.className = kind
          }
        })
      })
      nodes.push(unitPoint(unit, currentUnit && currentUnit.entity_id))
    })
  })
  return nodes
}

const renderCurrent = (layers, currentUnit, preWidth) => {
  const nodes = []
  if (!currentUnit) {
    return nodes
  }
  layers.forEach(layer => {
    layer.forEach(unit => {
      if (unit.id !== currentUnit.entity_id) {
        return
      }
      nodes.push(
        line({
          className: 'name-line',
          x1: preWidth,
          y1: unit.y,
          x2: unit.x + radius,
          y2: unit.y,
          'stroke-width': 2,
        })
      )
      nodes.push(
        text(
          {
            className: 'tree__current-unit',
            x: preWidth,
            y: unit.y + 6,
          },
          currentUnit.name
        )
      )
    })
  })
  return nodes
}

const renderLayers = ({ layers, currentUnit, preWidth, buckets }) => {
  let nodes = []
  // TODO-3 break into smaller functions, and there's lots of repetition..
  // This is done twice to ensure a line never covers over a circle
  nodes = nodes.concat(renderLines(layers))
  nodes = nodes.concat(renderPoints(layers, buckets, currentUnit))
  nodes = nodes.concat(renderCurrent(layers, currentUnit, preWidth))
  return nodes
}

module.exports = data => {
  let width
  const id = data.routeArgs[0]
  const treeData = data.subjectTrees && data.subjectTrees[id]

  if (!treeData) {
    return spinner()
  }

  const asLearner = data.route.indexOf('as_learner') > -1
  const asContrib = !asLearner

  let layers = orderLayers(putUnitsInLayers(treeData.units))
  const nodeHeight = layers.length
  const nodeWidth = Math.max.apply(null, layers.map(l => l.length))
  const preWidth = nodeWidth * radius * 2 + (nodeWidth + 1) * distance
  width = preWidth
  if (data.currentTreeUnit) {
    width += 12 * (6 * 2 + 5)
  }
  const height = nodeHeight * radius * 2 + (nodeHeight + 1) * distance
  layers = calculatePoints(layers, nodeWidth)

  const currentUnit = treeData.units.find(
    u => u.entity_id === data.currentTreeUnit
  )

  return div(
    { id: 'tree', className: 'page' },
    h1(`Tree: ${treeData.subjects.name}`),
    asContrib
      ? p(
          a(
            { href: `/subjects/${id}` },
            icon('subject'),
            ' View subject information'
          )
        )
      : null,
    p('You can click the nodes to see the unit name.'),
    svg(
      {
        className: 'tree',
        width,
        height,
      },
      renderLayers({
        layers,
        currentUnit,
        preWidth,
        buckets: treeData.buckets,
      })
    )
  )
}



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






module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .tree circle'(e, el) {
      if (e) e.preventDefault()
      if (el.classList.contains('selected')) {
        getTasks().selectTreeUnit()
      } else {
        getTasks().selectTreeUnit(el.id)
      }
    },

    'click .tree text'(e) {
      if (e) e.preventDefault()
      getTasks().selectTreeUnit()
    },
  })
}
*/
