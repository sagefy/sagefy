/*
const { div, p } = require('../../helpers/tags')

const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const entityRelationships = require('../components/entity_relationships.tmpl')
const spinner = require('../components/spinner.tmpl')
const previewUnitContent = require('../components/preview_unit_content.tmpl')

// TODO-2 This page should show a list of cards that the unit contains

module.exports = data => {
  const id = data.routeArgs[0]
  const unit = data.units && data.units[id]

  if (!unit) {
    return spinner()
  }

  const unitVersions = data.unitVersions && data.unitVersions[id]
  const topics = Object.keys(data.topics)
    .filter(topicId => data.topics[topicId].entity_id === id)
    .map(topicId => data.topics[topicId])

  return div(
    { id: 'unit', className: 'page' },
    followButton('unit', unit.entity_id, data.follows),
    entityHeader('unit', unit),
    p({ className: 'unit__body' }, unit.body),
    previewUnitContent(
      Object.assign({}, unit, {
        requires: unit.require_ids.map(rid => ({ id: rid })),
      })
    ),
    /* TODO-2 h2('Stats'),
    ul(
      li('Number of Learners: ???'),
      li('Quality: ???'),
      li('Difficulty: ???')
    ), /
    entityRelationships('unit', unit),
    entityTopics('unit', unit.entity_id, topics),
    entityVersions('unit', unit.entity_id, unitVersions)
  )
}





const { header, span, h1 } = require('../../helpers/tags')
const titleize = require('../../helpers/titleize')
const icon = require('./icon.tmpl')

module.exports = (kind, entity) => {
  let title = titleize(kind)
  if (kind === 'card') {
    title = `${titleize(entity.kind)} ${title}`
  }

  return header(
    { className: 'entity-header' },
    span({ className: 'entity-header__kind' }, icon(kind), ` ${title}`),
    h1(entity.name)
  )
}






const { h2, ul, li, a } = require('../../helpers/tags')

const verbage = {
  requires: 'Requires',
  required_by: 'Required by',
  belongs_to: 'Belongs to',
}

// const order = ['card', 'unit', 'subject']

const findKind = (curr, rel) => {
  if (rel === 'belongs_to') {
    if (curr === 'unit') {
      return 'subject'
    }

    if (curr === 'card') {
      return 'unit'
    }
  }

  return curr
}

module.exports = (kind, entity) => [
  h2('Relationships'),
  ul(
    entity.relationships.map(relation => {
      kind = findKind(kind, relation.kind)
      return li(
        verbage[relation.kind],
        ': ',
        a(
          { href: `/${kind}s/${relation.entity.entity_id}` },
          relation.entity.name
        )
      )
    })
  ),
]




const { div, a, h2, ul, li, p } = require('../../helpers/tags')
const timeago = require('./timeago.tmpl')
const icon = require('./icon.tmpl')

module.exports = (kind, entityID, topics) =>
  div(
    { className: 'entity-topics' },
    h2('Topics'),
    a(
      {
        href: `/topics/create?kind=${kind}&id=${entityID}`,
      },
      icon('create'),
      ' Create a new topic'
    ),
    topics && topics.length
      ? ul(
          topics.map(topic =>
            li(
              timeago(topic.created, { right: true }),
              // TODO-2 update time ago to latest post time
              a({ href: `/topics/${topic.id}` }, topic.name)
              // TODO-3 number of posts
            )
          ),
          li(
            a(
              { href: `/search?kind=topic&q=${entityID}` },
              '... See more topics ',
              icon('next')
            )
          )
        )
      : null,
    topics && topics.length ? null : p('No topics yet.')
  )




const capitalize = require('lodash.capitalize')
const { h2, ul, li, span, a } = require('../../helpers/tags')
const timeago = require('./timeago.tmpl')
const icon = require('./icon.tmpl')

module.exports = (kind, entityID, versions) => [
  h2('Versions'),
  ul(
    { className: 'entity-versions' },
    versions &&
      versions.map(version =>
        li(
          timeago(version.created, { right: true }),
          span(
            {
              className: `entity-versions__status--${version.status}`,
            },
            capitalize(version.status)
          ),
          ' ',
          version.name
        )
      ),
    li(
      a(
        { href: `/${kind}s/${entityID}/versions` },
        '... See more version history ',
        icon('next')
      )
    )
  ),
]
*/
