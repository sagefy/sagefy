const { header, span, h1 } = require('../../modules/tags')
const { ucfirst } = require('../../modules/auxiliaries')
const icon = require('./icon.tmpl')

module.exports = (kind, entity) => {
    let title = ucfirst(kind)
    if (kind === 'card') {
        title = ucfirst(entity.kind) + ' ' + title
    }

    return header(
        { className: 'entity-header' },
        span(
            { className: 'entity-header__kind' },
            icon(kind),
            ' ' + title
        ),
        h1(entity.name)
    )
}
