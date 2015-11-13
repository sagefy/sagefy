{div, h1, p, img, figure, h3, header,
 ul, li, a, strong, span} = require('../../modules/tags')
{timeAgo, truncate, ucfirst} = require('../../modules/auxiliaries')

module.exports = (data) ->
    [id] = data.routeArgs
    user = data.users?[id]
    return div({className: 'spinner'}) unless user

    return div(
        {id: 'profile', className: 'col-6'}
        header(
            img({src: user.avatar, className: 'avatar'})
            h1(user.name)
            p({className: 'timeago'}, 'Joined ' + timeAgo(user.created))
        )
        sets(user, user.sets) if user.sets
        follows(user, user.follows) if user.follows
        posts(user, user.posts) if user.posts
    )

sets = (user, sets) ->
    return [
        h3("#{user.name} is learning:")
        ul(
            li(a(
                {href: "/sets/#{set.id}"}
                set.name
            )) for set in sets
        )
    ]
    # TODO and link to search

follows = (user, follows) ->
    return [
        h3("#{user.name} follows:")
        ul(
            li(
                strong(ucfirst(follow.entity.kind))
                ': '
                a(
                    {href: "/#{follow.entity.kind}s/#{follow.entity.id}"}
                    'TODO follow.entity.name'
                )
            ) for follow in follows
        )
    ]
    # TODO and link to search

posts = (user, posts) ->
    return [
        h3("#{user.name} wrote:")
        ul(
            {className: 'posts'}
            li(
                strong(ucfirst(post.kind))
                ': '
                a(
                    {href: "/topics/#{post.topic_id}##{post.id}"}
                    truncate(post.body, 40)
                )
                span(
                    {className: 'timeago'}
                    timeAgo(post.created)
                )
                # TODO add topic info
            ) for post in posts
        )
    ]
    # TODO and link to search
