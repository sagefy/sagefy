const {div, p, h2, ul, li, a} = require('../../modules/tags')
const c = require('../../modules/content').get
const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = (data) => {
    const id = data.routeArgs[0]
    const set = data.sets && data.sets[id]

    if(!set) { return spinner() }

    // const following = data.follows &&
    //            data.follows.find((f) => f.entity.id === set.entity_id)

    return div(
        {id: 'set'},

        followButton('set', set.entity_id, data.follows),
        entityHeader('set', set),

        p(set.body),

        ul(
            li(`Language: ${c(set.language)}`),
            li(`Tags: ${set.tags.join(', ')}`)
        ),

        h2('Stats'),
        ul(
            li('Number of Learners: ???'),
            li('Quality: ???'),
            li('Difficulty: ???')
        ),

        h2({className: 'set__list-units-h2'}, 'List of Units'),
        a(
            {href: `/sets/${set.entity_id}/tree`},
            icon('set'),
            ' View Tree'
        ),
        ul(
            set.units.map(unit => li(a(
                {href: `/units/${unit.entity_id}`},
                unit.name
            )))
        ),

        entityTopics('set', set.entity_id, set.topics),
        entityVersions('set', set.entity_id, set.versions)
    )
}
