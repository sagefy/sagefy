const {div, ul, li, p, h2} =
    require('../../modules/tags')
const c = require('../../modules/content').get

const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const entityRelationships = require('../components/entity_relationships.tmpl')
const spinner = require('../components/spinner.tmpl')

// TODO-2 This page should show a list of cards that the unit contains

module.exports = (data) => {
    const id = data.routeArgs[0]
    const unit = data.units && data.units[id]

    if(!unit) { return spinner() }

    return div(
        {id: 'unit', className: 'page'},
        followButton('unit', unit.entity_id, data.follows),
        entityHeader('unit', unit),
        p(unit.body),
        ul(
            li(`Language: ${c(unit.language)}`),
            li(`Tags: ${unit.tags.join(', ')}`)
        ),
        h2('Stats'),
        ul(
            li('Number of Learners: ???'),
            li('Quality: ???'),
            li('Difficulty: ???')
        ),
        entityRelationships('unit', unit),
        entityTopics('unit', unit.entity_id, unit.topics),
        entityVersions('unit', unit.entity_id, unit.versions)
    )
}
