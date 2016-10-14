const {header, h3, hgroup, div, h1, ul, a} = require('../../modules/tags')
// const c = require('../../modules/content').get
const post = require('../components/post.tmpl')
const followButton = require('../components/follow_button.tmpl')
const {ucfirst} = require('../../modules/auxiliaries')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

// TODO-2 User doesn't show right after creating a new post in the topic view

module.exports = (data) => {
    const id = data.routeArgs[0]
    const posts = data.topicPosts && data.topicPosts[id]
    const topic = data.topics && data.topics[id]

    if (!topic || !posts) { return spinner() }

    return div(
        {id: 'topic'},

        header(
            followButton('topic', id, data.follows),
            hgroup(
                entity(topic, data),
                h1(topic.name),
                data.currentUserID === topic.user_id ? a(
                    {href: `/topics/${topic.id}/update`},
                    icon('update'),
                    ' Update name'
                ) : null
            )
        ),

        ul({className: 'posts'}, posts.map(p => post(p, data.currentUserID))),

        div(
            {className: 'topic__actions'},
            a(
                {
                    className: 'topic__create',
                    href: `/topics/${id}/posts/create`
                },
                icon('create'),
                ' Create a new post'
            )
        )
        // TODO-2 Pagination
    )
}

const entity = (topic, data) => {
    const entityKind = topic.entity.kind
    const entityID = topic.entity.id
    const entityObj = entityKind === 'card' ? data.cards[entityID]
                  : entityKind === 'unit' ? data.units[entityID]
                  : entityKind === 'set' ? data.sets[entityID]
                  : ''
    return h3(`${ucfirst(entityKind)}: ${entityObj.name}`)
}
