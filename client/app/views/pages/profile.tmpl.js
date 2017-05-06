const {div, h1, p, img, h3, header, ul, li} = require('../../modules/tags')
const {
  timeAgo,
  /* TP@ truncate,*/
} = require('../../modules/auxiliaries')
const spinner = require('../components/spinner.tmpl')
// TP@ const timeago = require('../components/timeago.tmpl')
const previewSubjectHead = require('../components/preview_subject_head.tmpl')
const previewUnitHead = require('../components/preview_unit_head.tmpl')
const previewCardHead = require('../components/preview_card_head.tmpl')

module.exports = (data) => {
    const [id] = data.routeArgs
    const user = data.users && data.users[id]
    if(!user) { return spinner() }

    return div(
        {id: 'profile', className: 'page'},
        header(
            {className: 'profile__header'},
            img({src: user.avatar, className: 'profile__avatar'}),
            h1(user.name),
            p('Joined ' + timeAgo(user.created))
        ),
        user.subjects ? showSubjects(user, user.subjects) : null,
        user.follows ? showFollows(user, user.follows) : null
        // TP@ user.posts ? showPosts(user, user.posts) : null
    )
}

const showSubjects = (user, subjects) =>
    [
        h3(`${user.name} is learning:`),
        ul(
            {className: 'profile__options'},
            subjects.map(subject => li(
                previewSubjectHead({
                    url: `/subjects/${subject.entity_id}`,
                    name: subject.name,
                    body: subject.body,
                })
            ))
        )
    ]
    // TODO-2 and link to search

const showFollows = (user, follows) =>
    [
        h3(`${user.name} follows:`),
        ul(
            {className: 'profile__options'},
            follows.map((follow) => {
                const e = follow.entity
                const kind = e.kind
                return li(
                    kind === 'subject' ?
                        previewSubjectHead({
                            url: `/subjects/${e.id}`,
                            name: e.id, // TODO-2 update to real name & body
                        }) :
                    kind === 'unit' ?
                        previewUnitHead({
                            url: `/units/${e.id}`,
                            name: e.id,
                        }) :
                    kind === 'card' ?
                        previewCardHead({
                            url: `/cards/${e.id}`,
                            name: e.id,
                        }) :
                        null
                )
            })
        )
        // TODO-2 and link to search
    ]

/*
TP@
const showPosts = (user, posts) =>
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
*/
