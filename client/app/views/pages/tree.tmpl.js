const {div, h1, a, p} = require('../../modules/tags')
const {svg, circle, line, text} = require('../../modules/svg_tags')
const {
    putUnitsInLayers,
    orderLayers,
    calculatePoints,
    findUnit
} = require('./tree.fn')
const {matchesRoute} = require('../../modules/auxiliaries')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

// TODO-2 show the learner their overall set progress as a percent or bar

const radius = 9
const distance = 36

module.exports = (data) => {
    let width
    const id = data.routeArgs[0]
    const treeData = data.setTrees && data.setTrees[id]

    if(!treeData) { return spinner() }

    const asLearner = data.route.indexOf('as_learner') > -1
    const asContrib = !asLearner

    let layers = orderLayers(putUnitsInLayers(treeData.units))
    const nodeHeight = layers.length
    const nodeWidth = Math.max.apply(null, layers.map((l) => l.length))
    const preWidth = width = nodeWidth * radius * 2 + (nodeWidth + 1) * distance
    if (data.currentTreeUnit) { width += 12 * (6 * 2 + 5) }
    const height = nodeHeight * radius * 2 + (nodeHeight + 1) * distance
    layers = calculatePoints(layers, nodeWidth)

    const currentUnit = treeData.units.find((u) =>
        u.entity_id === data.currentTreeUnit)

    let chooseUnitID
    let cardID
    if (data.next) {
        chooseUnitID = matchesRoute(data.next.path, '/s/sets/{id}/units')[0]
        cardID = matchesRoute(data.next.path, '/s/cards/{id}/learn')[0]
    }

    return div(
        {id: 'tree'},
        h1(`Tree: ${treeData.set.name}`),
        asContrib ? p(a(
            {href: `/sets/${id}`},
            icon('back'),
            ' View set information'
        )) : null,
        svg(
            {
                class: 'tree',
                xmlns: 'http://www.w3.org/2000/svg',
                version: '1.1',
                width,
                height,
            },
            renderLayers({
                layers,
                currentUnit,
                preWidth,
                buckets: treeData.buckets
            })
        ),
        chooseUnitID ? p(a(
            {
                className: 'tree__continue',
                href: `/sets/${chooseUnitID}/choose_unit`,
            },
            'Next ',
            icon('next')
        )) : null,
        cardID ? p(a(
            {className: 'tree__continue', href: `/cards/${cardID}/learn`},
            'Next ',
            icon('next')
        )) : null
    )
}

const renderLayers = ({layers, currentUnit, preWidth, buckets}) => {
    let nodes = []
    // TODO-3 break into smaller functions, and there's lots of repetition..
    // This is done twice to ensure a line never covers over a circle
    nodes = nodes.concat(renderLines(layers))
    nodes = nodes.concat(renderPoints(layers, buckets, currentUnit))
    nodes = nodes.concat(renderCurrent(layers, currentUnit, preWidth))
    return nodes
}

const renderLines = (layers) => {
    const nodes = []
    layers.forEach(layer => {
        layer.forEach(unit => {
            unit.requires.forEach(req => {
                req = findUnit(layers, req)
                nodes.push(unitLine({
                    x1: req.x,
                    y1: req.y,
                    x2: unit.x,
                    y2: unit.y
                }))
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
    if(!currentUnit) { return nodes }
    layers.forEach(layer => {
        layer.forEach(unit => {
            if(unit.id !== currentUnit.entity_id) { return }
            nodes.push(line({
                class: 'name-line',
                x1: preWidth,
                y1: unit.y,
                x2: unit.x + radius,
                y2: unit.y,
                'stroke-width': 2,
            }))
            nodes.push(text(
                {
                    class: 'tree__current-unit',
                    x: preWidth,
                    y: unit.y + 6
                },
                currentUnit.name
            ))
        })
    })
    return nodes
}

const unitPoint = ({id, x, y, className}, currentTreeUnit) =>
    circle({
        class: className + (currentTreeUnit === id ? ' selected' : ''),
        id,
        cx: x,
        cy: y,
        r: radius,
    })

const unitLine = ({x1, y1, x2, y2}) =>
    line({
        class: 'unit-require',
        x1,
        y1,
        x2,
        y2,
        'stroke-width': 2
    })
