/*

const capitalize = require('lodash.capitalize')
const { a, h3, span, ul, li, em, h4 } = require('../../helpers/tags')
const icon = require('./icon.tmpl')
const timeago = require('./timeago.tmpl')
const c = require('../../helpers/content').get

function hasValue(val) {
  return typeof val !== 'undefined' && val !== null
}

const shared = {
  previewName({ name, kind, url, labelKind, cardKindLabel }) {
    const label = labelKind
      ? cardKindLabel
        ? span(
            { className: 'preview__kind-label' },
            icon(kind),
            ' ',
            `${capitalize(cardKindLabel)} ${capitalize(kind)}`
          )
        : span(
            { className: 'preview__kind-label' },
            icon(kind),
            ' ',
            capitalize(kind)
          )
      : icon(kind)
    return url ? h3(label, ' ', a({ href: url }, name)) : h3(label, ' ', name)
  },

  previewCreated(created) {
    return created ? timeago(created, { right: true }) : null
  },

  previewStatus(status) {
    return status
      ? span(
          { className: `preview__status--${status}` },
          icon(
            status === 'accepted'
              ? 'good'
              : status === 'blocked'
                ? 'bad'
                : status === 'declined' ? 'bad' : 'progress'
          ),
          ' ',
          capitalize(status)
        )
      : null
  },

  previewAvailable(available) {
    return hasValue(available)
      ? available
        ? span({ className: 'preview__available' }, icon('good'), ' Available')
        : span({ className: 'preview__hidden' }, icon('bad'), ' Hidden')
      : null
  },

  previewLanguage(language) {
    return language
      ? span({ className: 'preview__language' }, 'Language: ', em(c(language)))
      : null
  },

  previewCommon({ created, status, available, language }) {
    return [
      shared.previewCreated(created),
      shared.previewStatus(status),
      shared.previewAvailable(available),
      shared.previewLanguage(language),
    ]
  },

  previewRequires(requires) {
    // url name id
    return requires && requires.length
      ? [
          h4('Requires'),
          ul(
            requires.map(require =>
              li(
                require.url
                  ? a({ href: require.url }, require.name || require.id)
                  : require.name || require.id
              )
            )
          ),
        ]
      : null
  },

  previewTags(tags) {
    return tags && tags.length ? span(`Tags: ${tags.join(', ')}`) : null
  },
}

module.exports = shared







const { div } = require('../../helpers/tags')
const previewSubjectHead = require('./preview_subject_head.tmpl')
const previewSubjectContent = require('./preview_subject_content.tmpl')

module.exports = function previewSubject(data) {
  return div(
    { className: 'preview--subject' },
    previewSubjectHead(data),
    previewSubjectContent(data)
  )
}


const capitalize = require('lodash.capitalize')
const { div, ul, li, a, h4, span } = require('../../helpers/tags')
const { previewCommon, previewTags } = require('./preview_shared.fn')
const icon = require('./icon.tmpl')

// TODO-2 show diff option

module.exports = function previewSubjectContent({
  status,
  available,
  created,
  language,
  members, // units and subjects: kind url name id
  units, // just a list of units: url name id
  tags,
}) {
  return div(
    { className: 'preview--subject__content' },
    previewCommon({ created, status, available, language }),
    units && units.length
      ? [
          h4('List of Units'),
          ul(
            units.map(unit =>
              li(
                unit.url
                  ? a({ href: unit.url }, unit.name || unit.id)
                  : unit.name || unit.id
              )
            )
          ),
        ]
      : null,
    members && members.length
      ? [
          h4('List of Members'),
          ul(
            { className: 'preview--subject__content__members' },
            members.map(member =>
              li(
                member.kind
                  ? [
                      span(
                        {
                          className: 'preview--subject__content__members__kind',
                        },
                        icon(member.kind),
                        ` ${capitalize(member.kind)}`
                      ),
                      ' ',
                    ]
                  : null,
                member.url
                  ? a({ href: member.url }, member.name || member.id)
                  : member.name || member.id
              )
            )
          ),
        ]
      : null,
    previewTags(tags)
  )
}



const { div, p } = require('../../helpers/tags')
const { previewName } = require('./preview_shared.fn')

module.exports = function previewSubjectHead({
  name,
  body,
  url = false,
  labelKind = false,
}) {
  return div(
    { className: 'preview--subject__head' },
    previewName({ name, kind: 'subject', url, labelKind }),
    body ? p(body) : null
  )
}

*/
