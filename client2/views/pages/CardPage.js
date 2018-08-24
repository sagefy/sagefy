/*
const { div, h2, ul, li } = require('../../helpers/tags')
const spinner = require('../components/spinner.tmpl')
const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const entityRelationships = require('../components/entity_relationships.tmpl')

const scored = [
  'choice',
  'number',
  'match',
  'formula',
  'writing',
  'upload',
  'embed',
]
const threeDigits = num => Math.round(num * 1000) / 1000

const previewCardContent = require('../components/preview_card_content.tmpl')

module.exports = data => {
  const id = data.routeArgs[0]
  const card = data.cards && data.cards[id]
  if (!card) {
    return spinner()
  }
  const cardVersions = data.cardVersions && data.cardVersions[id]

  const topics = Object.keys(data.topics)
    .filter(topicId => data.topics[topicId].entity_id === id)
    .map(topicId => data.topics[topicId])

  const params = card.card_parameters || {}
  const scr = card.kind in scored
  return div(
    { id: 'card', className: 'page' },
    followButton('card', card.entity_id, data.follows),
    entityHeader('card', card),
    previewCardContent(card),
    h2('Stats'),
    ul(
      li(`Number of Learners: ${params.num_learners}`),
      scr ? li(`Guess: ${threeDigits(params.guess)}`) : null,
      scr ? li(`Slip: ${threeDigits(params.slip)}`) : null,
      li(`Transit: ${threeDigits(params.transit)} (Default)`)
    ),
    entityRelationships('card', card),
    entityTopics('card', card.entity_id, topics),
    entityVersions('card', card.entity_id, cardVersions)
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
