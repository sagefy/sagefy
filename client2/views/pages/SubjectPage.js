/*


const { div, p, a } = require('../../helpers/tags')
const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const previewSubjectContent = require('../components/preview_subject_content.tmpl')

module.exports = data => {
  const id = data.routeArgs[0]
  const subject = data.subjects && data.subjects[id]

  if (!subject) {
    return spinner()
  }

  // const following = data.follows &&
  //      data.follows.find((f) => f.entity_id === subject.entity_id)

  const subjectVersions = data.subjectVersions && data.subjectVersions[id]
  const topics = Object.keys(data.topics)
    .filter(topicId => data.topics[topicId].entity_id === id)
    .map(topicId => data.topics[topicId])

  return div(
    { id: 'subject', className: 'page' },
    followButton('subject', subject.entity_id, data.follows),
    entityHeader('subject', subject),
    p({ className: 'subject__body' }, subject.body),
    previewSubjectContent({
      status: subject.status,
      available: subject.available,
      created: subject.created,
      language: subject.language,
      members: subject.members, // units and subjects: kind url name id
      units:
        subject.units &&
        subject.units.map(unit => ({
          name: unit.name,
          url: `/units/${unit.entity_id}`,
        })), // just a list of units: url name id
      tags: subject.tags,
    }),
    /* TODO-2 h2('Stats'),
    ul(
      li('Number of Learners: ???'),
      li('Quality: ???'),
      li('Difficulty: ???')
    ), /
    p(
      a(
        { href: `/subjects/${subject.entity_id}/tree` },
        icon('subject'),
        ' View Unit Tree'
      )
    ),
    entityTopics('subject', subject.entity_id, topics),
    entityVersions('subject', subject.entity_id, subjectVersions)
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
