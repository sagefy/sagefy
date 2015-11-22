{header, h3, hgroup, div, h1, ul, a, i, p} = require('../../modules/tags')
c = require('../../modules/content').get
post = require('../components/post.tmpl')
followButton = require('../components/follow_button.tmpl')
{ucfirst} = require('../../modules/auxiliaries')

module.exports = (data) ->
    id = data.routeArgs[0]
    posts = data.topicPosts?[id]
    topic = data.topics?[id]

    return div({className: 'spinner'}) unless topic and posts

    return div(
        {id: 'topic', className: 'col-8'}

        header(
            followButton('topic', id, data.follows)
            hgroup(
                entity(topic, data)
                h1(topic.name)
            )
        )

        ul({className: 'posts'}, post(p, data.currentUserID) for p in posts)

        div(
            {className: 'topic__actions'}
            a(
                {
                    className: 'button--good'
                    href: "/posts/create?topic_id=#{id}"
                }
                i({className: 'fa fa-plus'})
                ' Create a new post'
            )
        )
        # TODO Pagination
    )

entity = (topic, data) ->
    entityKind = topic.entity.kind
    entityID = topic.entity.id
    entity = if entityKind is 'card' then data.cards[entityID] \
             else if entityKind is 'unit' then data.units[entityID] \
             else if entityKind is 'set' then data.sets[entityID] \
             else ''
    return h3("#{ucfirst(entityKind)}: #{entity.name}")
