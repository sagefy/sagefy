const {div, p, a} = require('../../modules/tags')
const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const previewSetContent = require('../components/preview_set_content.tmpl')

module.exports = (data) => {
    const id = data.routeArgs[0]
    const set = data.sets && data.sets[id]

    if(!set) { return spinner() }

    // const following = data.follows &&
    //            data.follows.find((f) => f.entity.id === set.entity_id)

    return div(
        {id: 'set', className: 'page'},

        followButton('set', set.entity_id, data.follows),
        entityHeader('set', set),

        p({className: 'set__body'}, set.body),
        previewSetContent({
            status: set.status,
            available: set.available,
            created: set.created,
            language: set.language,
            members: set.members,  // units and sets: kind url name id
            units: set.units.map(unit => ({
                name: unit.name,
                url: `/units/${unit.entity_id}`,
            })),  // just a list of units: url name id
            tags: set.tags,
        }),

        /* TODO-2 h2('Stats'),
        ul(
            li('Number of Learners: ???'),
            li('Quality: ???'),
            li('Difficulty: ???')
        ), */

        a(
            {href: `/sets/${set.entity_id}/tree`},
            icon('set'),
            ' View Unit Tree'
        ),

        entityTopics('set', set.entity_id, set.topics),
        entityVersions('set', set.entity_id, set.versions)
    )
}
