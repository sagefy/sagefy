{header, h3, hgroup, div, h1, ul, a, i, p} = require('../../modules/tags')
c = require('../../modules/content').get
post = require('../components/post.tmpl')
followButton = require('../components/follow_button.tmpl')
{ucfirst} = require('../../modules/auxiliaries')
spinner = require('../components/spinner.tmpl')
icon = require('../components/icon.tmpl')

# TODO-2 User doesn't show right after creating a new post in the topic view

module.exports = (data) ->
    id = data.routeArgs[0]
    posts = data.topicPosts?[id]
    topic = data.topics?[id]

    return spinner() unless topic and posts

    return div(
        {id: 'topic'}

        header(
            followButton('topic', id, data.follows)
            hgroup(
                entity(topic, data)
                h1(topic.name)
                a(
                    {href: "/topics/#{topic.id}/update"}
                    icon('update')
                    ' Update name'
                )if data.currentUserID is topic.user_id
            )
        )

        ul({className: 'posts'}, post(p, data.currentUserID) for p in posts)

        div(
            {className: 'topic__actions'}
            a(
                {
                    className: 'topic__create'
                    href: "/topics/#{id}/posts/create"
                }
                icon('create')
                ' Create a new post'
            )
        )
        # TODO-2 Pagination
    )

entity = (topic, data) ->
    entityKind = topic.entity.kind
    entityID = topic.entity.id
    entity_ = if entityKind is 'card' then data.cards[entityID] \
              else if entityKind is 'unit' then data.units[entityID] \
              else if entityKind is 'set' then data.sets[entityID] \
              else ''
    return h3("#{ucfirst(entityKind)}: #{entity_.name}")
