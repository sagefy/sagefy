const { div, p, a } = require('../../modules/tags')
const followButton = require('../components/follow_button.tmpl')
const entityHeader = require('../components/entity_header.tmpl')
const entityTopics = require('../components/entity_topics.tmpl')
const entityVersions = require('../components/entity_versions.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const previewSubjectContent =
    require('../components/preview_subject_content.tmpl')

module.exports = (data) => {
    const id = data.routeArgs[0]
    const subject = data.subjects && data.subjects[id]

    if (!subject) { return spinner() }

    // const following = data.follows &&
    //            data.follows.find((f) => f.entity.id === subject.entity_id)

    const subjectVersions = data.subjectVersions && data.subjectVersions[id]

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
            members: subject.members,  // units and subjects: kind url name id
            units: subject.units.map(unit => ({
                name: unit.name,
                url: `/units/${unit.entity_id}`,
            })),  // just a list of units: url name id
            tags: subject.tags,
        }),

        /* TODO-2 h2('Stats'),
        ul(
            li('Number of Learners: ???'),
            li('Quality: ???'),
            li('Difficulty: ???')
        ), */
        p(
            a(
                { href: `/subjects/${subject.entity_id}/tree` },
                icon('subject'),
                ' View Unit Tree'
            )
        ),

        entityTopics('subject', subject.entity_id, subject.topics),
        entityVersions('subject', subject.entity_id, subjectVersions)
    )
}
