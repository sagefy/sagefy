/* eslint-disable camelcase */
const {
    div,
    a,
    iframe,
    ul,
    li,
    strong,
    small,
    span,
    em,
    h4,
} = require('../../modules/tags')
const { ucfirst } = require('../../modules/auxiliaries')
const {
    previewCommon,
    previewRequires,
    previewTags,
} = require('./preview_shared.fn')
const icon = require('./icon.tmpl')
const format = require('../../modules/format')
// TODO-2 show diff option

module.exports = function previewCardContent({
    kind,
    status,
    available,
    created,
    language,
    unit, // name, url = false
    data: {
        // video fields
        video_id,
        site,
        // choice fields
        body, // also for page kind
        options, // [{correct, value, feedback}]
        order,
        maxOptionsToShow,
        // unscored embed fields
        url,
    } = {},
    // then all...
    requires,
    tags,
}) {
    return div(
        { className: `preview--card__content preview--card__content--${kind}` },
        previewCommon({ created, status, available, language }),
        unit
            ? h4(
                  unit.url
                      ? a({ href: unit.url }, 'Unit: ', em(unit.name))
                      : span('Unit: ', em(unit.name))
              )
            : null,
        video_id && site === 'youtube'
            ? iframe({
                src:
                      `https://www.youtube.com/embed/${video_id}` +
                      '?autoplay=0&modestbranding=1&rel=0',
                width: 300,
                height: 200,
                allowfullscreen: true,
            })
            : null,
        url
          ? iframe({
            src: url,
            width: 300,
            height: 200,
          })
          : null,
        body ? div(format(body, { highestHeading: 2 })) : null,
        options && options.length
            ? ul(
                  options.map(option =>
                      li(
                          icon(option.correct ? 'good' : 'bad'),
                          ' ',
                          strong(option.value),
                          ' ',
                          small(`(${option.feedback})`)
                      )
                  )
              )
            : null,
        order ? span('Order: ', em(ucfirst(order))) : null,
        maxOptionsToShow
            ? span('Max Options To Show: ', em(maxOptionsToShow))
            : null,
        previewRequires(requires),
        previewTags(tags)
    )
}
