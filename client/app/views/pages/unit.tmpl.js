const { div, p } = require('../../modules/tags')

const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const entityRelationships = require('../components/entity_relationships.tmpl')
const spinner = require('../components/spinner.tmpl')
const previewUnitContent = require('../components/preview_unit_content.tmpl')

// TODO-2 This page should show a list of cards that the unit contains

module.exports = (data) => {
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
        requires: unit.require_ids.map(id => ({ id })),
      })
    ),
    /* TODO-2 h2('Stats'),
    ul(
      li('Number of Learners: ???'),
      li('Quality: ???'),
      li('Difficulty: ???')
    ), */
    entityRelationships('unit', unit),
    entityTopics('unit', unit.entity_id, topics),
    entityVersions('unit', unit.entity_id, unitVersions)
  )
}
