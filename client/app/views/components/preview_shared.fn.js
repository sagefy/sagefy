const {a, h3, span, ul, li} = require('../../modules/tags')
const {ucfirst} = require('../../modules/utilities')
const icon = require('./icon.tmpl')
const timeago = require('./timeago.tmpl')
const c = require('../../modules/content').get

function hasValue(val) {
    return typeof val !== 'undefined' && val !== null
}

const shared = {
    previewName(name, kind, url) {
        return url ?
            a({href: url}, h3(icon(kind), ` ${name}`)) :
            h3(icon(kind), ` ${name}`)
    },

    previewCreated(created) {
        return created ? timeago(created, {right: true}) : null
    },

    previewStatus(status) {
        return status ? span(
            {className: `preview__status--${status}`},
            ucfirst(status)
        ) : null
    },

    previewAvailable(available) {
        return hasValue(available) ?
            available ?
                span({className: 'preview__available'}, 'Available') :
                span({className: 'preview__hidden'}, 'Hidden')
            : null
    },

    previewLanguage(language) {
        return language ?
            span({className: 'preview__available'}, `Language: ${c(language)}`)
            : null
    },

    previewCommon({created, status, available, language}) {
        return [
            shared.previewCreated(created),
            shared.previewStatus(status),
            shared.previewAvailable(available),
            shared.previewLanguage(language),
        ]
    },

    previewRequires(requires) { // url name id
        return requires && requires.length ? ul(
            requires.map(require => li(
                require.url ?
                    a({href: require.url}, require.name || require.id) :
                    require.name || require.id
            ))
        ) : null
    },

    previewTags(tags) {
        return tags && tags.length ? span(`Tags: ${tags.join(', ')}`) : null
    },
}

module.exports = shared
