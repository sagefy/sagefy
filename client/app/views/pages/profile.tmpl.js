const {div, h1, p, img, h3, header,
 ul, li, a, strong} = require('../../modules/tags')
const {timeAgo, truncate, ucfirst} = require('../../modules/auxiliaries')
const spinner = require('../components/spinner.tmpl')
const timeago = require('../components/timeago.tmpl')

module.exports = (data) => {
    const [id] = data.routeArgs
    const user = data.users && data.users[id]
    if(!user) { return spinner() }

    return div(
        {id: 'profile'},
        header(
            {className: 'profile__header'},
            img({src: user.avatar, className: 'profile__avatar'}),
            h1(user.name),
            p('Joined ' + timeAgo(user.created))
        ),
        user.sets ? sets(user, user.sets) : null,
        user.follows ? follows(user, user.follows) : null,
        user.posts ? posts(user, user.posts) : null
    )
}

const sets = (user, sets) =>
    [
        h3(`${user.name} is learning:`),
        ul(
            sets.map(set => li(a(
                {href: `/sets/${set.id}`},
                set.name
            )))
        )
    ]
    // TODO-2 and link to search

const follows = (user, follows) =>
    [
        h3(`${user.name} follows:`),
        ul(
            follows.map(follow => li(
                strong(ucfirst(follow.entity.kind)),
                ': ',
                a(
                    {href: `/${follow.entity.kind}s/${follow.entity.id}`},
                    'TODO-2 follow.entity.name'
                )
            ))
        )
    ]
    // TODO-2 and link to search

const posts = (user, posts) =>
    [
        h3(`${user.name} wrote:`),
        ul(
            {className: 'posts'},
            posts.map(post => li(
                strong(ucfirst(post.kind)),
                ': ',
                a(
                    {href: `/topics/${post.topic_id}#${post.id}`},
                    truncate(post.body, 40)
                ),
                timeago(post.created, {right: true})
                // TODO-2 add topic info
            ))
        )
    ]
    // TODO-2 and link to search
