const {div, a, iframe, p, ul, li, strong, small, span} =
    require('../../modules/tags')
const {previewCommon, previewRequires, previewTags} =
    require('./preview_shared.fn')
const icon = require('./icon.tmpl')
// TODO-2 show diff option

module.exports = function previewCardContent({
    kind,
    status,
    available,
    created,
    language,
    unit, // name, url = false
    // video fields
    videoId,
    videoSite,
    // choice fields
    body,
    options, // [{correct, value, feedback}]
    order,
    maxOptionsToShow,
    // then all...
    requires,
    tags,
}) {
    return div(
        {className: `preview--card__content preview--card__content--${kind}`},
        previewCommon({created, status, available, language}),
        unit ?
          unit.url ?
            a({href: unit.url}, `Unit: ${unit.name}`)
            : `Unit: ${unit.name}`
          : null,
        videoId && videoSite === 'youtube' ? iframe({
            src: `https://www.youtube.com/embed/${videoId}` +
                 '?autoplay=0&modestbranding=1&rel=0',
            width: 300,
            height: 200,
            allowfullscreen: true,
        }) : null,
        body ? p(body) : null,
        options && options.length ? ul(options.map(option => li(
            icon(option.correct ? 'good' : 'bad'), ' ',
            strong(option.value), ' ',
            small(`(${option.feedback})`)
        ))) : null,
        order ? span(`Order: ${order}`) : null,
        maxOptionsToShow ?
          span(`Max Options To Show: ${maxOptionsToShow}`) :
          null,
        previewRequires(requires),
        previewTags(tags)
    )
}
